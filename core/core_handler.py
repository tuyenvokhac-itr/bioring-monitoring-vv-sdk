from typing import List, Tuple, Optional

from bleak import BLEDevice, AdvertisementData, BleakClient
from numpy.f2py.auxfuncs import throw_error

from ble.ble_constant import BleConstant
from ble.ble_manager import BleManager
from ble.bt_device import BTDevice
from errors.common_error import CommonError
from managers.bluetooth_callback import BluetoothCallback
import logging


class CoreHandler:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(CoreHandler, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._init_logger()
        self.ble_manager = BleManager()
        self.devices: List[Tuple[BLEDevice, AdvertisementData]] = []
        self.clients: List[BleakClient] = []
        self.bluetooth_callback: Optional[BluetoothCallback] = None
        self.is_scanning = False

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
                return

    def on_bluetooth_error(self, address, error: CommonError):
        device = next((d for d in self.devices if d[0].address == address), None)
        self.bluetooth_callback.on_bluetooth_error(
            BTDevice(name=device[0].name, address=device[0].address), error)

    async def disconnect(self, address: str):
        client = next((cl for cl in self.clients if cl.address == address), None)

        if client is None:
            self.logger.error('[CoreHandler]: Could not find client with address %s', address)
            throw_error('Could not find client')
            return

        await self.ble_manager.disconnect(client)

    def on_device_disconnected(self, client: BleakClient):
        self.clients.remove(client)
        self.logger.info('[CoreHandler]: Device DISCONNECTED: %s', client)
        device = next((d for d in self.devices if d[0].address == client.address), None)
        self.bluetooth_callback.on_bluetooth_error(
            BTDevice(name=device[0].name, address=device[0].address), CommonError.DEVICE_DISCONNECTED)