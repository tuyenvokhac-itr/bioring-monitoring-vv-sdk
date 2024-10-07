import asyncio
import logging
import time
from functools import partial
from typing import List, Tuple, Optional, Callable

from bleak import BLEDevice, AdvertisementData, BleakClient
from numpy.f2py.auxfuncs import throw_error

from ble.ble_constant import BleConstant
from ble.ble_manager import BleManager
from ble.bt_device import BTDevice
from core.callbacks.response_callback import ResponseCallback
from core.callbacks.streaming_callback import StreamingCallback
from core.command.bluetooth_settings.set_bluetooth_settings_command import SetBluetoothSettingsCommand
from core.command.data_recording.get_record import GetRecordCommand
from core.command.data_recording.get_record_sample_threshold_command import GetRecordSampleThresholdCommand
from core.command.data_recording.start_record import StartRecordCommand
from core.command.data_recording.stop_record import StopRecordCommand
from core.command.dfu.enter_dfu_command import EnterDfuCommand
from core.command.general.get_device_info_command import GetDeviceInfoCommand
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
from core.command.streaming_raw_data.live_acc_data_command import LiveAccDataCommand
from core.command.streaming_raw_data.live_ecg_data_command import LiveEcgDataCommand
from core.command.streaming_raw_data.live_ppg_data_command import LivePpgDataCommand
from core.command.streaming_raw_data.live_temp_data_command import LiveTempDataCommand
from core.command.streaming_raw_data.stop_streaming_data_command import StopStreamingDataCommand
from core.command.time_syncing.get_time_syncing_command import GetTimeSyncingCommand
from core.command.time_syncing.set_time_syncing_command import SetTimeSyncingCommand
from core.enum.sensor_type import SensorType
from core.handler.dfu.dfu_handler import DfuHandler
from core.handler.rx_char_handler import RxCharHandler
from core.models.device_info import DeviceInfo
from core.models.device_status import DeviceStatus
from core.models.protocol import Protocol
from core.models.raw_data.accel_data import AccelData
from core.models.raw_data.ecg_data import EcgData
from core.models.raw_data.ppg_data import PpgData
from core.models.raw_data.samples_threshold import SamplesThreshold
from core.models.raw_data.temp_data import TempData
from core.models.self_tests.self_test_result import SelfTestResult
from core.models.settings.accel_settings import AccelSettings
from core.models.settings.bt_settings import BTSettings
from core.models.settings.device_settings import DeviceSettings
from core.models.settings.ecg_settings import EcgSettings
from core.models.settings.log_settings import LogSettings
from core.models.settings.ppg_settings import PpgSettings
from core.utils.singleton import singleton
from errors.common_error import CommonError
from errors.common_result import CommonResult
from managers.bluetooth_callback import BluetoothCallback
from managers.record_data_callback import RecordDataCallback


@singleton
class CoreHandler:
    def __init__(self):
        self._init_logger()
        self.ble_manager = BleManager()
        self.bluetooth_callback: Optional[BluetoothCallback] = None
        self.is_scanning = False
        self.response_callbacks: List[ResponseCallback] = []
        self.streaming_callbacks: List[StreamingCallback] = []
        self.record_data_callbacks: List[RecordDataCallback] = []

        """ devices: found devices"""
        self.devices: List[Tuple[BLEDevice, AdvertisementData]] = []

        """ clients: connected devices"""
        self.clients: List[BleakClient] = []

    def _init_logger(self):
        self.logger = logging.getLogger(__name__)
        c_handler = logging.StreamHandler()
        self.logger.addHandler(c_handler)
        self.logger.setLevel(logging.DEBUG)

    def set_bluetooth_callback(self, callback: BluetoothCallback):
        self.bluetooth_callback = callback

    """ BLE functions """

    async def start_scan(self):
        if self.is_scanning:
            return
        self.logger.info('[CoreHandler]: Start scan...')
        self.is_scanning = True
        self.devices.clear()
        await self.ble_manager.start_scan(self._on_device_found)

    def _on_device_found(self, device: BLEDevice, advertisement_data: AdvertisementData):
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
        self.devices = []
        self.logger.info('[CoreHandler]: Scan stopped')

    async def connect(self, address: str, timeout: int = 10):
        await self.ble_manager.connect(
            address,
            timeout,
            self._on_device_connected,
            self._on_device_disconnected,
            self._on_bluetooth_error,
        )

    def _on_device_connected(self, client: BleakClient):
        self.logger.info('[CoreHandler]: Device connected: %s', client)

        try:
            device: Optional[BTDevice] = None
            # Find device in self.devices
            for d in self.devices:
                if d[0].address == client.address:
                    device = BTDevice(address=d[0].address, name=d[0].name)
                    self.clients.append(client)
                    self.bluetooth_callback.on_device_connected(device)
                    break

            if device is None:
                self.logger.error('[CoreHandler]: Could not find device with address %s', client.address)
                throw_error('Could not find device')
                return

            rx_chars_handler = RxCharHandler(
                device=device,
                response_callbacks=self.response_callbacks,
                streaming_callbacks=self.streaming_callbacks
            )
            asyncio.create_task(
                self.ble_manager.start_notify(
                    BleConstant.BRS_UUID_CHAR_RX,
                    client,
                    rx_chars_handler.handle
                )
            )

        except Exception as e:
            self.logger.error('[CoreHandler]: Error on device connected: %s', e)

    def _on_bluetooth_error(self, address, error: CommonError):
        device = self._get_device(address)
        self.bluetooth_callback.on_bluetooth_error(
            BTDevice(name=device[0].name, address=device[0].address),
            error
        )

    async def disconnect(self, address: str):
        client = self._get_client(address)

        if client is None:
            self.logger.error('[CoreHandler]: Could not find client with address %s', address)
            return

        await self.ble_manager.disconnect(client)

    def _on_device_disconnected(self, client: BleakClient):
        self.clients.remove(client)
        self.logger.info('[CoreHandler]: Device DISCONNECTED: %s', client)
        device = self._get_device(client.address)
        self.bluetooth_callback.on_bluetooth_error(
            BTDevice(name=device[0].name, address=device[0].address),
            CommonError.DEVICE_DISCONNECTED
        )

    def _get_device(self, address: str):
        device = next((d for d in self.devices if d[0].address == address), None)
        if device is None:
            self.logger.error('[CoreHandler]: Could not find device with address %s', address)
            throw_error('Could not find device')

        return device

    def _get_client(self, address: str):
        client = next((cl for cl in self.clients if cl.address == address), None)
        if client is None:
            self.logger.error('[CoreHandler]: Could not find client with address %s', address)
            throw_error('Could not find client')

        return client

    """ Command functions """

    """ Bluetooth settings """

    async def set_bluetooth_settings(
            self,
            address: str,
            settings: BTSettings,
            on_success: Callable[[CommonResult], None]
    ):
        client = self._get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await SetBluetoothSettingsCommand.send(sid, client, settings, self.ble_manager.write_char)

    """ Self tests """

    async def get_post(
            self,
            address: str,
            on_self_test_result: Callable[[CommonResult, Optional[SelfTestResult]], None]
    ):
        client = self._get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_self_test_result))
        await GetPostCommand.send(sid, client, self.ble_manager.write_char)

    async def get_bist(
            self,
            address: str,
            on_self_test_result: Callable[[CommonResult, Optional[SelfTestResult]], None]
    ):
        client = self._get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_self_test_result))
        await GetBistCommand.send(sid, client, self.ble_manager.write_char)

    async def enable_bist(self, address: str, on_success: Callable[[CommonResult], None]):
        client = self._get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await EnableBistCommand.send(sid, client, self.ble_manager.write_char)

    async def disable_bist(self, address: str, on_success: Callable[[CommonResult], None]):
        client = self._get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await DisableBistCommand.send(sid, client, self.ble_manager.write_char)

    async def set_bist_interval(self, address: str, interval: int, on_success: Callable[[CommonResult], None]):
        client = self._get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await SetBistIntervalCommand.send(sid, client, interval, self.ble_manager.write_char)

    """ Streaming data """

    async def start_streaming_accel_data(
            self,
            address: str,
            on_accel_streaming_data: Callable[[CommonResult, Optional[AccelData], int], None] = None,
    ):
        client = self._get_client(address)
        sid = int(time.time() * 1000)
        self.streaming_callbacks.append(StreamingCallback(sid, SensorType.ACCEL, on_accel_streaming_data))
        await LiveAccDataCommand.send(sid, client, True, self.ble_manager.write_char)

    async def start_streaming_ecg_data(
            self,
            address: str,
            on_ecg_streaming_data: Callable[[CommonResult, Optional[EcgData], int], None] = None,
    ):
        client = self._get_client(address)
        sid = int(time.time() * 1000)
        self.streaming_callbacks.append(StreamingCallback(sid, SensorType.ECG, on_ecg_streaming_data))
        await LiveEcgDataCommand.send(sid, client, True, self.ble_manager.write_char)

    async def start_streaming_ppg_data(
            self,
            address: str,
            on_ppg_streaming_data: Callable[[CommonResult, Optional[PpgData], int], None] = None,
    ):
        client = self._get_client(address)
        sid = int(time.time() * 1000)
        self.streaming_callbacks.append(StreamingCallback(sid, SensorType.PPG, on_ppg_streaming_data))
        await LivePpgDataCommand.send(sid, client, True, self.ble_manager.write_char)

    async def start_streaming_temp_data(
            self,
            address: str,
            on_temp_streaming_data: Callable[[CommonResult, Optional[TempData], int], None] = None,
    ):
        client = self._get_client(address)
        sid = int(time.time() * 1000)
        self.streaming_callbacks.append(StreamingCallback(sid, SensorType.TEMP, on_temp_streaming_data))
        await LiveTempDataCommand.send(sid, client, True, self.ble_manager.write_char)

    async def stop_streaming_data(
            self,
            address: str,
            sensor_type: SensorType,
            on_success: Callable[[CommonResult], None]
    ):
        client = self._get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await StopStreamingDataCommand.send(
            sid=sid,
            client=client,
            sensor_type=sensor_type,
            write_char=self.ble_manager.write_char
        )

    """ Data recording """

    async def get_record_samples_threshold(
            self,
            address: str,
            on_record_samples_threshold: Callable[[CommonResult, Optional[SamplesThreshold]], None]
    ):
        client = self._get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_record_samples_threshold))
        await GetRecordSampleThresholdCommand.send(sid, client, self.ble_manager.write_char)

    async def start_record(
            self,
            address: str,
            samples: int,
            sensor_type: SensorType,
            on_success: Callable[[CommonResult], None]
    ):
        client = self._get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await StartRecordCommand.send(sid, client, samples, sensor_type, self.ble_manager.write_char)

    async def stop_record(
            self,
            address: str,
            sensor_type: SensorType,
            on_success: Callable[[CommonResult], None]
    ):
        client = self._get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await StopRecordCommand.send(sid, client, sensor_type, self.ble_manager.write_char)

    async def get_record(self, address: str, sensor_type: SensorType, start_index: int):
        client = self._get_client(address)
        sid = int(time.time() * 1000)
        await GetRecordCommand.send(sid, client, start_index, sensor_type, self.ble_manager.write_char)

    def set_record_callback(self, callback: RecordDataCallback):
        self.record_data_callbacks.append(callback)

    def remove_record_callback(self, callback: RecordDataCallback):
        self.record_data_callbacks.remove(callback)

    """ Device settings """

    async def get_all_settings(
            self,
            address: str,
            on_settings: Callable[[CommonResult, Optional[DeviceSettings]], None]
    ):
        client = self._get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_settings))
        await GetAllSettingsCommand.send(sid, client, self.ble_manager.write_char)

    async def set_log_settings(
            self,
            address: str,
            settings: LogSettings,
            on_success: Callable[[CommonResult], None]
    ):
        client = self._get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await SetLogSettingsCommand.send(sid, client, settings, self.ble_manager.write_char)

    """ Sensor settings """

    async def set_ecg_settings(
            self,
            address: str,
            settings: EcgSettings,
            on_success: Callable[[CommonResult], None]
    ):
        client = self._get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await SetEcgSettingsCommand.send(sid, client, settings, self.ble_manager.write_char)

    async def set_ppg_settings(
            self,
            address: str,
            settings: PpgSettings,
            on_success: Callable[[CommonResult], None]
    ):
        client = self._get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await SetPpgSettingsCommand.send(sid, client, settings, self.ble_manager.write_char)

    async def set_accel_settings(
            self,
            address: str,
            settings: AccelSettings,
            on_success: Callable[[CommonResult], None]
    ):
        client = self._get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await SetAccelSettingsCommand.send(sid, client, settings, self.ble_manager.write_char)

    """ Firmware update """

    async def update_firmware(
            self,
            address: str,
            dfu_path: str,
            on_success: Callable[[CommonResult], None]
    ):
        client = self._get_client(address)
        device = self._get_device(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(
            ResponseCallback(
                sid,
                partial(self._on_enter_dfu_success, device, dfu_path, on_success),
                # lambda: self._on_enter_dfu_success(dfu_path, client, on_success)
            )
        )
        await EnterDfuCommand.send(sid, client, self.ble_manager.write_char)

    def _on_enter_dfu_success(
            self,
            device: Tuple[BLEDevice, AdvertisementData],
            dfu_path: str,
            on_success: Callable[[CommonResult], None],
            result: CommonResult
    ):
        # handle when result is failed
        dfu_handler = DfuHandler(
            device=device,
            dfu_file_path=dfu_path,
            on_dfu_result=on_success
        )
        pass

    """ Power management """

    async def set_sleep_time(
            self,
            address: str,
            seconds: int,
            on_success: Callable[[CommonResult], None]
    ):
        client = self._get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await SetSleepTimeCommand.send(sid, client, seconds, self.ble_manager.write_char)

    """ Time syncing """

    async def set_time_sync(self, address: str, epoch: int, on_success: Callable[[CommonResult], None]):
        client = self._get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await SetTimeSyncingCommand.send(sid, client, epoch, self.ble_manager.write_char)

    async def get_time_sync(self, address: str, on_time_sync: Callable[[CommonResult, Optional[int]], None]):
        client = self._get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_time_sync))
        await GetTimeSyncingCommand.send(sid, client, self.ble_manager.write_char)

    """ General """

    async def get_device_info(
            self,
            address: str,
            on_device_info: Callable[[CommonResult, Optional[DeviceInfo]], None]
    ):
        client = self._get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_device_info))
        await GetDeviceInfoCommand.send(sid, client, self.ble_manager.write_char)

    async def get_device_status(
            self,
            address: str,
            on_device_status: Callable[[CommonResult, Optional[DeviceStatus]], None]
    ):
        client = self._get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_device_status))
        await GetDeviceStatusCommand.send(sid, client, self.ble_manager.write_char)

    async def get_protocol_info(
            self,
            address: str,
            on_protocol_info: Callable[[CommonResult, Optional[Protocol]], None]
    ):
        client = self._get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_protocol_info))
        await GetProtocolInfoCommand.send(sid, client, self.ble_manager.write_char)

    """ Reset """

    async def factory_reset(self, address: str, on_success: Callable[[CommonResult], None]):
        client = self._get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await FactoryResetCommand.send(sid, client, self.ble_manager.write_char)

    async def reboot(self, address: str, on_success: Callable[[CommonResult], None]):
        client = self._get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await RebootCommand.send(sid, client, self.ble_manager.write_char)
