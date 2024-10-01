from abc import ABC, abstractmethod
from typing import Callable, Optional

from core.enum.sensor_type import SensorType
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
from errors.common_result import CommonResult
from managers.bluetooth_callback import BluetoothCallback
from managers.record_data_callback import RecordDataCallback


class RingManager(ABC):
    """ ************************************ BLE APIs ********************************** """

    """
    Start scanning for Bluetooth devices. 
    Device satisfies the condition will be returned in BluetoothCallback.on_scan_result.
    Refer to managers/bluetooth_callback.py (BluetoothCallback) for more information. 
    """

    @abstractmethod
    def start_scan(self):
        pass

    """
    Stop scanning for Bluetooth devices.
    """

    @abstractmethod
    def stop_scan(self):
        pass

    """
    Connect to the Bluetooth device with the given address.
    If the connection is successful, BluetoothCallback.on_device_connected will be called.
    If the connection is unsuccessful, BluetoothCallback.on_bluetooth_error will be called.
    Refer to managers/bluetooth_callback.py (BluetoothCallback) for more information. 
    """

    @abstractmethod
    def connect(self, address: str, timeout: int):
        pass

    """
    Disconnect from the Bluetooth device with the given address.
    """

    @abstractmethod
    def disconnect(self, address: str):
        pass

    """
    Check the current state of Bluetooth.
    Returns True if Bluetooth is on, False otherwise.
    """

    @abstractmethod
    def get_bluetooth_state(self) -> bool:
        pass

    """ 
    Set BluetoothCallback for to listen to Bluetooth events.
    Class desired to listen to Bluetooth events should implement BluetoothCallback interface.
    Refer to managers/bluetooth_callback.py (BluetoothCallback) for more information. 
    """

    @abstractmethod
    def set_bluetooth_callback(self, callback: BluetoothCallback):
        pass

    """ ********************************** Bluetooth Settings APIs ******************************** """

    @abstractmethod
    def set_bluetooth_settings(
            self,
            address: str,
            settings: BTSettings,
            on_success: Callable[[CommonResult], None],
    ):
        pass

    """ ********************************** Self Test APIs ******************************** """

    @abstractmethod
    def get_post(
            self,
            address: str,
            on_self_test_result: Callable[[CommonResult, Optional[SelfTestResult]], None]
    ):
        pass

    @abstractmethod
    def get_bist(
            self,
            address: str,
            on_self_test_result: Callable[[CommonResult, Optional[SelfTestResult]], None]
    ):
        pass

    @abstractmethod
    def enable_bist(self, address: str, on_success: Callable[[CommonResult], None]):
        pass

    @abstractmethod
    def disable_bist(self, address: str, on_success: Callable[[CommonResult], None]):
        pass

    @abstractmethod
    def set_bist_interval(
            self,
            address: str,
            interval: int,
            on_success: Callable[[CommonResult], None]
    ):
        pass

    """ ********************************** Streaming data APIs ******************************** """

    @abstractmethod
    def start_streaming_accel_data(
            self,
            address: str,
            on_accel_streaming_data: Callable[[CommonResult, Optional[AccelData], int], None] = None,
    ):
        pass

    @abstractmethod
    def start_streaming_ecg_data(
            self,
            address: str,
            on_ecg_streaming_data: Callable[[CommonResult, Optional[EcgData], int], None] = None,
    ):
        pass

    @abstractmethod
    def start_streaming_ppg_data(
            self,
            address: str,
            on_ppg_streaming_data: Callable[[CommonResult, Optional[PpgData], int], None] = None,
    ):
        pass

    @abstractmethod
    def start_streaming_temp_data(
            self,
            address: str,
            on_temp_streaming_data: Callable[[CommonResult, Optional[TempData], int], None] = None,
    ):
        pass

    @abstractmethod
    def stop_streaming_data(
            self,
            address: str,
            sensor_type: SensorType,
            on_success: Callable[[CommonResult], None]
    ):
        pass

    """ ********************************** Data Recording APIs ******************************** """

    @abstractmethod
    def get_record_samples_threshold(
            self,
            address: str,
            on_record_samples_threshold: Callable[[CommonResult, Optional[SamplesThreshold]], None]
    ):
        pass

    @abstractmethod
    def start_record(
            self,
            address: str,
            samples: int,
            sensor_type: SensorType,
            on_success: Callable[[CommonResult], None]
    ):
        pass

    @abstractmethod
    def stop_record(
            self, address: str,
            sensor_type: SensorType,
            on_success: Callable[[CommonResult], None]
    ):
        pass

    @abstractmethod
    def get_record(self, address: str, sensor_type: SensorType, start_index: int):
        pass

    @abstractmethod
    def set_record_callback(self, callback: RecordDataCallback):
        pass

    """ ********************************** Device Settings APIs ******************************** """

    @abstractmethod
    def get_all_settings(
            self,
            address: str,
            on_settings: Callable[[CommonResult, Optional[DeviceSettings]], None]
    ):
        pass

    @abstractmethod
    def set_log_settings(
            self,
            address: str,
            settings: LogSettings,
            on_success: Callable[[CommonResult], None]
    ):
        pass

    """ ********************************** Sensor Settings APIs ******************************** """

    @abstractmethod
    def set_ecg_settings(
            self,
            address: str,
            settings: EcgSettings,
            on_success: Callable[[CommonResult], None]
    ):
        pass

    @abstractmethod
    def set_ppg_settings(
            self,
            address: str,
            settings: PpgSettings,
            on_success: Callable[[CommonResult], None]
    ):
        pass

    @abstractmethod
    def set_accel_settings(
            self,
            address: str,
            settings: AccelSettings,
            on_success: Callable[[CommonResult], None]
    ):
        pass

    """ ********************************** Firmware Update APIs ******************************** """

    @abstractmethod
    def update_firmware(self, address: str, dfu_path: str, on_success: Callable[[CommonResult], None]):
        pass

    """ ********************************** Power Management APIs ******************************** """

    @abstractmethod
    def set_sleep_time(self, address: str, seconds: int, on_success: Callable[[CommonResult], None]):
        pass

    """ ********************************** Time Syncing APIs ******************************** """

    @abstractmethod
    def set_time_sync(self, address: str, epoch: int, on_success: Callable[[CommonResult], None]):
        pass

    @abstractmethod
    def get_time_sync(self, address: str, on_time_sync: Callable[[CommonResult, Optional[int]], None]):
        pass

    """ ********************************** General APIs ******************************** """

    @abstractmethod
    def get_device_info(
            self,
            address: str,
            on_device_info: Callable[[CommonResult, Optional[DeviceInfo]], None]
    ):
        pass

    @abstractmethod
    def get_device_status(
            self,
            address: str,
            on_device_status: Callable[[CommonResult, Optional[DeviceStatus]], None]
    ):
        pass

    @abstractmethod
    def get_protocol_info(
            self,
            address: str,
            on_protocol_info: Callable[[CommonResult, Optional[Protocol]], None]
    ):
        pass

    """ ********************************** Reset APIs ******************************** """

    @abstractmethod
    def factory_reset(self, address: str, on_success: Callable[[CommonResult], None]):
        pass

    @abstractmethod
    def reboot(self, address: str, on_success: Callable[[CommonResult], None]):
        pass
