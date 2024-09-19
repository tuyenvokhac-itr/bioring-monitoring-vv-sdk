import asyncio

from ble.ble_manager import BleManager
from core.core_handler import CoreHandler
from core.new_core_handler import NewCoreHandler
from managers.bluetooth_callback import BluetoothCallback
from managers.ring_manager_interface import RingManagerInterface


class RingManager(RingManagerInterface):
    def __init__(self):
        self.new_core_handler = NewCoreHandler()
        pass

    def start_scan(self):
        asyncio.create_task(self.new_core_handler.start_scan())

    def stop_scan(self):
        pass

    def connect(self, address: str, timeout: int):
        pass

    def disconnect(self, address: str):
        pass

    def get_bluetooth_state(self) -> bool:
        pass

    def set_bluetooth_callback(self, callback: BluetoothCallback):
        pass