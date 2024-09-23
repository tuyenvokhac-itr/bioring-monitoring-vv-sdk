import asyncio
import platform
from collections.abc import Callable

from core.core_handler import CoreHandler
from core.enum.sensor_type import SensorType
from core.models.bluetooth_settings.bt_settings import BTSettings
from core.models.raw_data.samples_threshold import SamplesThreshold
from core.models.self_tests.self_test_result import SelfTestResult
from errors.common_result import CommonResult
from managers.bluetooth_callback import BluetoothCallback
from managers.record_data_callback import RecordDataCallback
from managers.ring_manager_interface import RingManagerInterface
from ble.mac_bluetooth_state.mac_get_bluetooth_state import mac_get_bluetooth_state
from managers.streaming_data_callback import StreamingDataCallback


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
            return mac_get_bluetooth_state()
        """ TODO: Implement for Windows and Ubuntu """
        return False

    """ 
    Set BluetoothCallback for to listen to Bluetooth events.
    Class desired to listen to Bluetooth events should implement BluetoothCallback interface.
    Refer to managers/bluetooth_callback.py (BluetoothCallback) for more information. 
    """

    def set_bluetooth_callback(self, bluetooth_callback: BluetoothCallback):
        self.core_handler.set_callback(bluetooth_callback)

    """ ********************************** Bluetooth Settings APIs ******************************** """

    def set_bt_settings(
            self,
            address: str,
            settings: BTSettings,
            on_success: Callable[[CommonResult], None],
    ):
        # TODO: Implement this method
        pass

    """ ********************************** Self Test APIs ******************************** """

    def get_post(self, address: str, on_self_test_result: Callable[[SelfTestResult], None]):
        # TODO: Implement this method
        pass

    def get_bist(self, address: str, on_self_test_result: Callable[[SelfTestResult], None]):
        # TODO: Implement this method
        pass

    def enable_bist(self, address: str, on_success: Callable[[CommonResult], None]):
        # TODO: Implement this method
        pass

    def disable_bist(self, address: str, on_success: Callable[[CommonResult], None]):
        # TODO: Implement this method
        pass

    def set_bist_interval(self, address: str, interval: int, on_success: Callable[[CommonResult], None]):
        # TODO: Implement this method
        pass

    """ ********************************** Streaming data APIs ******************************** """

    def start_streaming_data(self, address: str, sensor_type: SensorType, on_success: Callable[[CommonResult], None]):
        # TODO: Implement this method
        pass

    def stop_streaming_data(self, address: str, sensor_type: SensorType, on_success: Callable[[CommonResult], None]):
        # TODO: Implement this method
        pass

    def set_streaming_data_callback(self, callback: StreamingDataCallback):
        # TODO: Implement this method
        pass

    """ ********************************** Data Recorder APIs ******************************** """

    def get_record_samples_threshold(self, address: str,
                                     on_record_samples_threshold: Callable[[SamplesThreshold], None]):
        # TODO: Implement this method
        pass

    def start_record(
            self, address: str,
            samples: int, sensor_type: SensorType,
            on_success: Callable[[CommonResult], None]
    ):
        # TODO: Implement this method
        pass

    def stop_record(
            self, address: str,
            samples: int, sensor_type: SensorType,
            on_success: Callable[[CommonResult], None]
    ):
        # TODO: Implement this method
        pass

    def get_record(self, address: str, sensor_type: SensorType, start_index: int):
        pass

    def set_record_callback(self, callback: RecordDataCallback):
        pass