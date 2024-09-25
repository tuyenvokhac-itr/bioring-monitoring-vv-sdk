from abc import ABC, abstractmethod
from typing import Callable, Optional

from core.enum.general_enum import SensorType
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
from errors.common_result import CommonResult
from managers.bluetooth_callback import BluetoothCallback
from managers.record_data_callback import RecordDataCallback
from managers.streaming_data_callback import StreamingDataCallback


class RingManagerInterface(ABC):
    """ ************************************ BLE APIs ********************************** """

    @abstractmethod
    def start_scan(self):
        pass

    @abstractmethod
    def stop_scan(self):
        pass

    @abstractmethod
    def connect(self, address: str, timeout: int):
        pass

    @abstractmethod
    def disconnect(self, address: str):
        pass

    @abstractmethod
    def get_bluetooth_state(self) -> bool:
        pass

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
    def get_post(self, address: str, on_self_test_result: Callable[[CommonResult, Optional[SelfTestResult]], None]):
        pass

    @abstractmethod
    def get_bist(self, address: str, on_self_test_result: Callable[[CommonResult, Optional[SelfTestResult]], None]):
        pass

    @abstractmethod
    def enable_bist(self, address: str, on_success: Callable[[CommonResult], None]):
        pass

    @abstractmethod
    def disable_bist(self, address: str, on_success: Callable[[CommonResult], None]):
        pass

    @abstractmethod
    def set_bist_interval(self, address: str, interval: int, on_success: Callable[[CommonResult], None]):
        pass

    """ ********************************** Streaming data APIs ******************************** """

    @abstractmethod
    def start_streaming_accel_data(
            self, address: str, on_success: Callable[[CommonResult], None] = None,
            on_accel_received: Callable[[AccelData, int], None] = None,
    ):
        pass

    @abstractmethod
    def start_streaming_ecg_data(
            self, address: str, on_success: Callable[[CommonResult], None] = None,
            on_ecg_received: Callable[[EcgData, int], None] = None,
    ):
        pass

    @abstractmethod
    def start_streaming_ppg_data(
            self, address: str, on_success: Callable[[CommonResult], None] = None,
            on_ppg_received: Callable[[PpgData, int], None] = None,
    ):
        pass

    @abstractmethod
    def start_streaming_temp_data(
            self, address: str, on_success: Callable[[CommonResult], None] = None,
            on_temp_received: Callable[[TempData, int], None] = None,
    ):
        pass

    @abstractmethod
    def stop_streaming_data(self, address: str, sensor_type: SensorType, on_success: Callable[[CommonResult], None]):
        pass

    @abstractmethod
    def set_streaming_data_callback(self, callback: StreamingDataCallback):
        pass

    """ ********************************** Data Recorder APIs ******************************** """

    @abstractmethod
    def get_record_samples_threshold(
            self, address: str,
            on_record_samples_threshold: Callable[[CommonResult, Optional[SamplesThreshold]], None]
    ):
        pass

    @abstractmethod
    def start_record(
            self, address: str,
            samples: int, sensor_type: SensorType,
            on_success: Callable[[CommonResult], None]
    ):
        pass

    @abstractmethod
    def stop_record(
            self, address: str,
            samples: int, sensor_type: SensorType,
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
    def get_all_settings(self, address: str, on_settings: Callable[[CommonResult, Optional[DeviceSettings]], None]):
        pass

    @abstractmethod
    def set_log_settings(self, address: str, settings: LogSettings, on_success: Callable[[CommonResult], None]):
        pass

    """ ********************************** Sensor Settings APIs ******************************** """

    @abstractmethod
    def set_ecg_settings(self, address: str, settings: EcgSettings, on_success: Callable[[CommonResult], None]):
        pass

    @abstractmethod
    def set_ppg_settings(self, address: str, settings: PpgSettings, on_success: Callable[[CommonResult], None]):
        pass

    @abstractmethod
    def set_accel_settings(self, address: str, settings: AccelSettings, on_success: Callable[[CommonResult], None]):
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
    def get_device_info(self, address: str, on_device_info: Callable[[CommonResult, Optional[DeviceInfo]], None]):
        pass

    @abstractmethod
    def get_device_status(self, address: str, on_device_status: Callable[[CommonResult, Optional[DeviceStatus]], None]):
        pass

    @abstractmethod
    def get_protocol_info(self, address: str, on_protocol_info: Callable[[CommonResult, Optional[Protocol]], None]):
        pass

    """ ********************************** Reset APIs ******************************** """

    @abstractmethod
    def factory_reset(self, address: str, on_success: Callable[[CommonResult], None]):
        pass

    @abstractmethod
    def reboot(self, address: str, on_success: Callable[[CommonResult], None]):
        pass
