from ble.ble_manager import BleManager
from typing import List, Tuple, Callable
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from core.core_handler_call_back import CoreHandlerCallBack
from bleak import BleakClient

class CoreHandler:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(CoreHandler, cls).__new__(cls)
        return cls._instance

    def __init__(self, core_handler_call_back: CoreHandlerCallBack):
        self.core_handler_call_back = core_handler_call_back
        self.ble_manager = BleManager()
        self.devices : List[Tuple[BLEDevice, AdvertisementData]] = []
    
    # 
    
    def start_scan(self) -> List[Tuple[BLEDevice, AdvertisementData]]:
        print("Start scan...")
        self.devices = self.ble_manager.scan()
        print(self.devices)

    # Support 1 device currently    
    def connect(self):
        for device in self.devices:
            self.ble_manager.connect(device[0].address, onDeviceConnected=self._on_device_connected)
            print('connecting')
    
    # Callback function
            
    def _on_device_connected(self, client: BleakClient):
        print('connected ${client.address}')
        self.core_handler_call_back.on_device_connected(client)