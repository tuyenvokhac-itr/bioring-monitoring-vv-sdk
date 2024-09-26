import logging
import time
from typing import List, Tuple, Optional, Callable

from bleak import BLEDevice, AdvertisementData, BleakClient
from numpy.f2py.auxfuncs import throw_error

import proto.brp_pb2 as brp
from ble.ble_constant import BleConstant
from ble.ble_manager import BleManager
from ble.bt_device import BTDevice
from core.command import GetDeviceInfoCommand, LiveAccDataCommand, LiveEcgDataCommand, LivePpgDataCommand, \
    LiveTempDataCommand
from core.command.bluetooth_settings.set_bluetooth_settings_command import SetBluetoothSettingsCommand
from core.command.data_recording.get_record import GetRecordCommand
from core.command.data_recording.get_record_sample_threshold_command import GetRecordSampleThresholdCommand
from core.command.data_recording.start_record import StartRecordCommand
from core.command.data_recording.stop_record import StopRecordCommand
from core.command.general.get_device_status_command import GetDeviceStatusCommand
from core.command.general.get_protocol_info_command import GetProtocolInfoCommand
from core.command.power_management.set_sleep_time_command import SetSleepTimeCommand
from core.command.reset.factory_reset_command import FactoryResetCommand
from core.command.reset.reboot_command import RebootCommand
from core.command.self_tests.disable_bist_command import DisableBistCommand
from core.command.self_tests.enable_bist_command import EnableBistCommand
from core.command.self_tests.get_bist_command import GetBistCommand
from core.command.self_tests.get_post_command import GetPostCommand
from core.command.self_tests.self_test_command import SetBistIntervalCommand
from core.command.settings.get_all_settings_command import GetAllSettingsCommand
from core.command.settings.set_accel_settings_command import SetAccelSettingsCommand
from core.command.settings.set_ecg_settings_command import SetEcgSettingsCommand
from core.command.settings.set_log_settings_command import SetLogSettingsCommand
from core.command.settings.set_ppg_settings_command import SetPpgSettingsCommand
from core.command.streaming_raw_data.stop_streaming_data_command import StopStreamingDataCommand
from core.command.time_syncing.get_time_syncing_command import GetTimeSyncingCommand
from core.command.time_syncing.set_time_syncing_command import SetTimeSyncingCommand
from core.command_callback import ResponseCallback
from core.enum.sensor_type import SensorType
from core.handler.proto.response.general.res_device_info_handler import ResDeviceInfoHandler
from core.handler.proto.response.general.res_device_status_handler import ResDeviceStatusHandler
from core.handler.proto.response.general.res_protocol_info_handler import ResProtocolInfoHandler
from core.handler.proto.response.res_common_result_handler import ResCommonResultHandler
from core.handler.proto.response.self_tests.res_bist_handler import ResBistHandler
from core.handler.proto.response.self_tests.res_post_handler import ResPostHandler

from core.handler.proto.response.settings.res_all_settings_handler import ResAllSettingsHandler
from core.handler.proto.response.time_syncing.res_time_syncing_handler import ResTimeSyncingHandler
from core.models import DeviceInfo, AccelData, EcgData, PpgData, TempData
from core.models.device_status import DeviceStatus
from core.models.protocol import Protocol
from core.models.raw_data.samples_threshold import SamplesThreshold
from core.models.self_tests.self_test_result import SelfTestResult
from core.models.settings.accel_settings import AccelSettings
from core.models.settings.bt_settings import BTSettings
from core.models.settings.device_settings import DeviceSettings
from core.models.settings.ecg_settings import EcgSettings
from core.models.settings.log_settings import LogSettings
from core.models.settings.ppg_settings import PpgSettings
from errors.common_error import CommonError
from errors.common_result import CommonResult
from managers.bluetooth_callback import BluetoothCallback
from managers.record_data_callback import RecordDataCallback


class CoreHandler:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(CoreHandler, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._init_logger()
        self.ble_manager = BleManager()
        self.bluetooth_callback: Optional[BluetoothCallback] = None
        self.is_scanning = False
        self.response_callbacks: List[ResponseCallback] = []

        """ devices: found devices"""
        self.devices: List[Tuple[BLEDevice, AdvertisementData]] = []

        """ clients: connected devices"""
        self.clients: List[BleakClient] = []

    def _init_logger(self):
        self.logger = logging.getLogger(__name__)
        c_handler = logging.StreamHandler()
        self.logger.addHandler(c_handler)
        self.logger.setLevel(logging.DEBUG)

    def set_callback(self, callback: BluetoothCallback):
        self.bluetooth_callback = callback

    """ BLE functions """

    async def start_scan(self):
        if self.is_scanning:
            return
        self.logger.info('[CoreHandler]: Start scan...')
        self.is_scanning = True
        self.devices.clear()
        await self.ble_manager.start_scan(self.on_device_found)

    def on_device_found(self, device: BLEDevice, advertisement_data: AdvertisementData):
        if device.name is not None and BleConstant.BIORING_PREFIX in device.name:
            # check if device is already in the list
            for d in self.devices:
                if d[0].address == device.address:
                    return

            self.devices.append((device, advertisement_data))
            self.bluetooth_callback.on_scan_result(BTDevice(address=device.address, name=device.name))

    async def stop_scan(self):
        await self.ble_manager.stop_scan()
        self.is_scanning = False
        self.logger.info('[CoreHandler]: Scan stopped')

    async def connect(self, address: str, timeout: int = 10):
        await self.ble_manager.connect(
            address,
            timeout,
            self.on_device_connected,
            self.on_device_disconnected,
            self.on_bluetooth_error,
        )

    def on_device_connected(self, client: BleakClient):
        self.logger.info('[CoreHandler]: Device connected: %s', client)

        # Find device in self.devices
        for d in self.devices:
            if d[0].address == client.address:
                device = BTDevice(address=d[0].address, name=d[0].name)
                self.clients.append(client)
                self.bluetooth_callback.on_device_connected(device)
                break

        self.ble_manager.start_notify(BleConstant.BRS_UUID_CHAR_RX, client, self.brs_rx_char_handler)
        self.ble_manager.start_notify(BleConstant.BRS_UUID_CHAR_DATA, client, self.brs_data_char_handler)

    def on_bluetooth_error(self, address, error: CommonError):
        device = self.get_device(address)
        self.bluetooth_callback.on_bluetooth_error(
            BTDevice(name=device[0].name, address=device[0].address), error)

    async def disconnect(self, address: str):
        client = self.get_client(address)

        if client is None:
            self.logger.error('[CoreHandler]: Could not find client with address %s', address)
            throw_error('Could not find client')
            return

        await self.ble_manager.disconnect(client)

    def on_device_disconnected(self, client: BleakClient):
        self.clients.remove(client)
        self.logger.info('[CoreHandler]: Device DISCONNECTED: %s', client)
        device = self.get_device(client.address)
        self.bluetooth_callback.on_bluetooth_error(
            BTDevice(name=device[0].name, address=device[0].address), CommonError.DEVICE_DISCONNECTED)

    def start_notify(self, client: BleakClient, char_uuid, callback):
        self.ble_manager.start_notify(char_uuid, client, callback)
        self.logger.info('[CoreHandler]: Start notify for %s', client.address)

    def brs_rx_char_handler(self, _sender, data: bytearray):
        rx_packet = brp.Packet()
        rx_packet.ParseFromString(bytes(data))
        logging.debug(f"Received packet:\n{rx_packet}")

        # TODO: check this if we can compare the PacketType value
        pkt_type = rx_packet.WhichOneof("payload")
        if pkt_type == "response":
            cid = rx_packet.response.cid
            self.rx_response_handlers(cid, rx_packet)

        elif pkt_type == "notification":
            nid = rx_packet.notification.nid
            if nid in self.rx_notif_handlers:
                self.rx_notif_handlers[nid](rx_packet)

    def brs_data_char_handler(self, _sender, data: bytearray):
        # | Type   | Sequence number | Length | Value   |
        # |--------|-----------------|--------|---------|
        # | 1 byte |    2 byte       | 2 byte | n bytes |

        # self.handle_streaming_data(data)
        pass

    def rx_response_handlers(self, cid: int, pkt: brp.Packet):
        match cid:
            case brp.CommandId.CID_DEV_INFO_GET:
                ResDeviceInfoHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_BLE_SETTINGS_SET:
                ResCommonResultHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_SELF_TEST_POST_GET:
                ResPostHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_SELF_TEST_BIST_GET:
                ResBistHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_SELF_TEST_BIST_ENABLE:
                ResCommonResultHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_SELF_TEST_BIST_DISABLE:
                ResCommonResultHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_SELF_TEST_BIST_SET_INTERVAL:
                ResCommonResultHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_ALL_SETTINGS_GET:
                ResAllSettingsHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_LOG_SETTINGS_SET:
                ResCommonResultHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_ECG_SETTINGS_SET:
                ResCommonResultHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_PPG_SETTINGS_SET:
                ResCommonResultHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_ACCEL_SETTINGS_SET:
                ResCommonResultHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_DEV_PRE_SLEEP_TIMEOUT_SET:
                ResCommonResultHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_TIME_SET:
                ResCommonResultHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_TIME_GET:
                ResTimeSyncingHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_DEV_INFO_GET:
                ResDeviceInfoHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_DEV_STATUS_GET:
                ResDeviceStatusHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_PROTOCOL_INFO_GET:
                ResProtocolInfoHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_DEV_FACTORY_RESET:
                ResCommonResultHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_REBOOT:
                ResCommonResultHandler.handle(pkt, self.response_callbacks)
            case _:
                pass

    def handle_notif_charging_status_changed(self, pkt: brp.Packet):
        self.core_handler_call_back.on_charging_info_received(pkt.notification.charging)
        logging.debug(f"[NT] Charging status: {pkt.notification.charging}")

    def handle_notif_battery_level_changed(self, pkt: brp.Packet):
        self.core_handler_call_back.on_battery_level_received(
            pkt.notification.battery_level
        )
        logging.debug(f"[NT] Battery level: {pkt.notification.battery_level}")

    rx_notif_handlers = {
        brp.NotificationId.NID_LOG_DATA: None,
        brp.NotificationId.NID_CHARGING_STATUS_CHANGED: handle_notif_charging_status_changed,
        brp.NotificationId.NID_BATTERY_LEVEL_CHANGED: handle_notif_battery_level_changed,
        # brp.NotificationId.NID_SPO2_HR_DATA: handle_noti_hr_spo2,
    }

    def handle_streaming_data(self, data: bytearray):
        # data_handler_map = {
        #     NotifyDataType.AFE: self.data_handler_afe,
        #     NotifyDataType.ACC: self.data_handler_imu,
        #     NotifyDataType.TEMP: self.data_handler_temperature,
        #     NotifyDataType.LOG: self.data_handler_log_resp,
        #     NotifyDataType.POWER: self.data_handle_power,
        #     NotifyDataType.SELF_TEST: self.data_handle_self_test,
        # }
        #
        # (data_type, sequence_number, length, value) = self.proto.decode_streaming_data(
        #     data
        # )
        # if data_type in data_handler_map:
        #     data_handler_map[data_type](value, length)

        return 0

    def get_device(self, address: str):
        device = next((d for d in self.devices if d[0].address == address), None)
        if device is None:
            self.logger.error('[CoreHandler]: Could not find device with address %s', address)
            throw_error('Could not find device')

        return device

    def get_client(self, address: str):
        client = next((cl for cl in self.clients if cl.address == address), None)
        if client is None:
            self.logger.error('[CoreHandler]: Could not find client with address %s', address)
            throw_error('Could not find client')

        return client

    def get_response_callback(self, sid: int):
        return next((cb for cb in self.response_callbacks if cb.sid == sid), None)

    """ Command functions """
    """ Bluetooth settings """

    async def set_bluetooth_settings(
            self, address: str, settings: BTSettings,
            on_success: Callable[[CommonResult], None]
    ):
        client = self.get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await SetBluetoothSettingsCommand.send(sid, client, settings, self.ble_manager.write_char)

    """ Self tests """

    async def get_post(
            self, address: str,
            on_self_test_result: Callable[[CommonResult, Optional[SelfTestResult]], None]
    ):
        client = self.get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_self_test_result))
        await GetPostCommand.send(sid, client, self.ble_manager.write_char)

    async def get_bist(
            self, address: str,
            on_self_test_result: Callable[[CommonResult, Optional[SelfTestResult]], None]
    ):
        client = self.get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_self_test_result))
        await GetBistCommand.send(sid, client, self.ble_manager.write_char)

    async def enable_bist(self, address: str, on_success: Callable[[CommonResult], None]):
        client = self.get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await EnableBistCommand.send(sid, client, self.ble_manager.write_char)

    async def disable_bist(self, address: str, on_success: Callable[[CommonResult], None]):
        client = self.get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await DisableBistCommand.send(sid, client, self.ble_manager.write_char)

    async def set_bist_interval(self, address: str, interval: int, on_success: Callable[[CommonResult], None]):
        client = self.get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await SetBistIntervalCommand.send(sid, client, interval, self.ble_manager.write_char)

    """ Streaming data """

    async def start_streaming_accel_data(
            self, address: str,
            on_success: Callable[[CommonResult], None] = None,
            on_accel_received: Callable[[AccelData, int], None] = None,
    ):
        client = self.get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await LiveAccDataCommand.send(sid, client, True, self.ble_manager.write_char)

    async def start_streaming_ecg_data(
            self, address: str,
            on_success: Callable[[CommonResult], None] = None,
            on_ecg_received: Callable[[EcgData, int], None] = None,
    ):
        client = self.get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await LiveEcgDataCommand.send(sid, client, True, self.ble_manager.write_char)

    async def start_streaming_ppg_data(
            self, address: str,
            on_success: Callable[[CommonResult], None] = None,
            on_ppg_received: Callable[[PpgData, int], None] = None,
    ):
        client = self.get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await LivePpgDataCommand.send(sid, client, True, self.ble_manager.write_char)

    async def start_streaming_temp_data(
            self, address: str,
            on_success: Callable[[CommonResult], None] = None,
            on_temp_received: Callable[[TempData, int], None] = None,
    ):
        client = self.get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await LiveTempDataCommand.send(sid, client, True, self.ble_manager.write_char)

    async def stop_streaming_data(
            self, address: str, sensor_type: SensorType,
            on_success: Callable[[CommonResult], None]
    ):
        client = self.get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await StopStreamingDataCommand.send(
            sid=sid, client=client, sensor_type=sensor_type,
            write_char=self.ble_manager.write_char
        )

    """ Data recording """

    async def get_record_samples_threshold(
            self, address: str,
            on_record_samples_threshold: Callable[[CommonResult, Optional[SamplesThreshold]], None]
    ):
        client = self.get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_record_samples_threshold))
        await GetRecordSampleThresholdCommand.send(sid, client, self.ble_manager.write_char)

    async def start_record(
            self, address: str,
            samples: int, sensor_type: SensorType,
            on_success: Callable[[CommonResult], None]
    ):
        client = self.get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await StartRecordCommand.send(sid, client, samples, sensor_type, self.ble_manager.write_char)

    async def stop_record(
            self, address: str,
            samples: int, sensor_type: SensorType,
            on_success: Callable[[CommonResult], None]
    ):
        client = self.get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await StopRecordCommand.send(sid, client, sensor_type, self.ble_manager.write_char)

    async def get_record(self, address: str, sensor_type: SensorType, start_index: int):
        client = self.get_client(address)
        sid = int(time.time() * 1000)
        await GetRecordCommand.send(sid, client, start_index, sensor_type, self.ble_manager.write_char)

    def set_record_callback(self, callback: RecordDataCallback):
        pass

    """ Device settings """

    async def get_all_settings(self, address: str,
                               on_settings: Callable[[CommonResult, Optional[DeviceSettings]], None]):
        client = self.get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_settings))
        await GetAllSettingsCommand.send(sid, client, self.ble_manager.write_char)

    async def set_log_settings(self, address: str, settings: LogSettings, on_success: Callable[[CommonResult], None]):
        client = self.get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await SetLogSettingsCommand.send(sid, client, settings, self.ble_manager.write_char)

    """ Sensor settings """

    async def set_ecg_settings(self, address: str, settings: EcgSettings, on_success: Callable[[CommonResult], None]):
        client = self.get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await SetEcgSettingsCommand.send(sid, client, settings, self.ble_manager.write_char)

    async def set_ppg_settings(self, address: str, settings: PpgSettings, on_success: Callable[[CommonResult], None]):
        client = self.get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await SetPpgSettingsCommand.send(sid, client, settings, self.ble_manager.write_char)

    async def set_accel_settings(
            self, address: str, settings: AccelSettings,
            on_success: Callable[[CommonResult], None]
    ):
        client = self.get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await SetAccelSettingsCommand.send(sid, client, settings, self.ble_manager.write_char)

    """ Firmware update """

    def update_firmware(self, address: str, dfu_path: str, on_success: Callable[[CommonResult], None]):
        client = self.get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))

    """ Power management """

    async def set_sleep_time(self, address: str, seconds: int, on_success: Callable[[CommonResult], None]):
        client = self.get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await SetSleepTimeCommand.send(sid, client, seconds, self.ble_manager.write_char)

    """ Time syncing """

    async def set_time_sync(self, address: str, epoch: int, on_success: Callable[[CommonResult], None]):
        client = self.get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await SetTimeSyncingCommand.send(sid, client, epoch, self.ble_manager.write_char)

    async def get_time_sync(self, address: str, on_time_sync: Callable[[CommonResult, Optional[int]], None]):
        client = self.get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_time_sync))
        await GetTimeSyncingCommand.send(sid, client, self.ble_manager.write_char)

    """ General """

    async def get_device_info(self, address: str, on_device_info: Callable[[CommonResult, Optional[DeviceInfo]], None]):
        client = self.get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_device_info))
        await GetDeviceInfoCommand.send(sid, client, self.ble_manager.write_char)

    async def get_device_status(self, address: str,
                                on_device_status: Callable[[CommonResult, Optional[DeviceStatus]], None]):
        client = self.get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_device_status))
        await GetDeviceStatusCommand.send(sid, client, self.ble_manager.write_char)

    async def get_protocol_info(self, address: str,
                                on_protocol_info: Callable[[CommonResult, Optional[Protocol]], None]):
        client = self.get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_protocol_info))
        await GetProtocolInfoCommand.send(sid, client, self.ble_manager.write_char)

    """ Reset """

    async def factory_reset(self, address: str, on_success: Callable[[CommonResult], None]):
        client = self.get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await FactoryResetCommand.send(sid, client, self.ble_manager.write_char)

    async def reboot(self, address: str, on_success: Callable[[CommonResult], None]):
        client = self.get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await RebootCommand.send(sid, client, self.ble_manager.write_char)
