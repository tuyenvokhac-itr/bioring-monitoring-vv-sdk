import asyncio
import time
from typing import List, Tuple, Optional, Callable

from bleak import BLEDevice, AdvertisementData, BleakClient
from numpy.f2py.auxfuncs import throw_error

from ble.ble_constant import BleConstant
from ble.ble_manager import BleManager
from ble.bt_device import BTDevice
from core.command import GetDeviceInfoCommand
from core.command.bluetooth_settings.set_bluetooth_settings_command import SetBluetoothSettingsCommand
from core.command.self_tests.self_test_command import SelfTestCommand
from core.command_callback import ResponseCallback
from core.handler.proto.response.res_device_info_handler import ResDeviceInfoHandler
from core.handler.proto.response.set_bluetooth_settings_handler import SetBluetoothSettingsHandler
from core.models import DeviceInfo
from core.models.self_tests.self_test_result import SelfTestResult
from core.models.settings.bt_settings import BTSettings
from errors.common_error import CommonError
from errors.common_result import CommonResult
from managers.bluetooth_callback import BluetoothCallback
import logging
import proto.brp_pb2 as brp


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
                SetBluetoothSettingsHandler.handle(pkt, self.response_callbacks)
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

    async def get_device_info(self, address: str, on_device_info: Callable[[CommonResult, Optional[DeviceInfo]], None]):
        client = self.get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_device_info))
        await GetDeviceInfoCommand.send(sid=sid, client=client, write_char=self.ble_manager.write_char)

    async def set_bluetooth_settings(
            self, address: str, settings: BTSettings,
            on_success: Callable[[CommonResult], None]
    ):
        client = self.get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_success))
        await SetBluetoothSettingsCommand.send(sid, client, settings, self.ble_manager.write_char)

    async def get_post(self, address: str, on_self_test_result: Callable[[CommonResult, Optional[SelfTestResult]], None]):
        client = self.get_client(address)
        sid = int(time.time() * 1000)
        self.response_callbacks.append(ResponseCallback(sid, on_self_test_result))
        await SelfTestCommand.get_post(sid, client, self.ble_manager.write_char)