from typing import List, Tuple

from bleak import BLEDevice, AdvertisementData

from ble.ble_manager import BleManager
from managers.bluetooth_callback import BluetoothCallback


class NewCoreHandler:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(NewCoreHandler, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.ble_manager = BleManager()
        self.devices: List[Tuple[BLEDevice, AdvertisementData]] = []

    async def start_scan(self):
        print("Start scan...")
        self.devices = await self.ble_manager.scan()
        print('hehe')
        print(self.devices)

