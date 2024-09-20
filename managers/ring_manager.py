import asyncio
import platform
from core.core_handler import CoreHandler
from managers.bluetooth_callback import BluetoothCallback
from managers.ring_manager_interface import RingManagerInterface
from ble.mac_bluetooth_state_checker import check_bluetooth_state_mac_os


class RingManager(RingManagerInterface):
    def __init__(self):
        self.core_handler = CoreHandler()

    """ ********************************** BLE APIs ******************************** """

    """
    Start scanning for Bluetooth devices. 
    Device satisfies the condition will be returned in BluetoothCallback.on_scan_result.
    Refer to managers/bluetooth_callback.py (BluetoothCallback) for more information. 
    """
    def start_scan(self):
        asyncio.create_task(self.core_handler.start_scan())

    """
    Stop scanning for Bluetooth devices.
    """
    def stop_scan(self):
        asyncio.create_task(self.core_handler.stop_scan())

    """
    Connect to the Bluetooth device with the given address.
    If the connection is successful, BluetoothCallback.on_device_connected will be called.
    If the connection is unsuccessful, BluetoothCallback.on_bluetooth_error will be called.
    Refer to managers/bluetooth_callback.py (BluetoothCallback) for more information. 
    """
    def connect(self, address: str, timeout: int = 10):
        asyncio.create_task(self.core_handler.connect(address, timeout))

    """
    Disconnect from the Bluetooth device with the given address.
    """
    def disconnect(self, address: str):
        asyncio.create_task(self.core_handler.disconnect(address))

    """
    Check the current state of Bluetooth.
    Returns True if Bluetooth is on, False otherwise.
    """
    def get_bluetooth_state(self) -> bool:
        if platform.system() == "Darwin":
            return check_bluetooth_state_mac_os()
        """ TODO: Implement for Windows and Ubuntu """
        return False

    """ 
    Set BluetoothCallback for to listen to Bluetooth events.
    Class desired to listen to Bluetooth events should implement BluetoothCallback interface.
    Refer to managers/bluetooth_callback.py (BluetoothCallback) for more information. 
    """
    def set_bluetooth_callback(self, bluetooth_callback: BluetoothCallback):
        self.core_handler.set_callback(bluetooth_callback)
