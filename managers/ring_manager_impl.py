import asyncio
import platform
from collections.abc import Callable
from typing import Optional

from ble.mac_bluetooth_state.mac_get_bluetooth_state import mac_get_bluetooth_state
from core.core_handler import CoreHandler
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
from core.utils.singleton import singleton
from errors.common_result import CommonResult
from managers.bluetooth_callback import BluetoothCallback
from managers.record_data_callback import RecordDataCallback
from managers.ring_manager import RingManager


@singleton
class _RingManagerImpl(RingManager):
    def __init__(self):
        self.core_handler = CoreHandler()

    """ ********************************** BLE APIs ******************************** """

    def start_scan(self):
        asyncio.create_task(self.core_handler.start_scan())

    def stop_scan(self):
        asyncio.create_task(self.core_handler.stop_scan())

    def connect(self, address: str, timeout: int = 10):
        asyncio.create_task(self.core_handler.connect(address, timeout))

    def disconnect(self, address: str):
        asyncio.create_task(self.core_handler.disconnect(address))

    def get_bluetooth_state(self) -> bool:
        if platform.system() == "Darwin":
            return mac_get_bluetooth_state()
        """ TODO: Implement for Windows and Ubuntu """
        return False

    def set_bluetooth_callback(self, bluetooth_callback: BluetoothCallback):
        self.core_handler.set_bluetooth_callback(bluetooth_callback)
        # TODO: Handle state listener

    """ ********************************** Bluetooth Settings APIs ******************************** """

    def set_bluetooth_settings(
            self,
            address: str,
            settings: BTSettings,
            on_result: Callable[[CommonResult], None],
    ):
        asyncio.create_task(self.core_handler.set_bluetooth_settings(address, settings, on_result))

    """ ********************************** Self Test APIs ******************************** """

    def get_post(
            self,
            address: str,
            on_self_test_result: Callable[[CommonResult, Optional[SelfTestResult]], None]
    ):
        asyncio.create_task(self.core_handler.get_post(address, on_self_test_result))

    def get_bist(
            self,
            address: str,
            on_self_test_result: Callable[[CommonResult, Optional[SelfTestResult]], None]
    ):
        asyncio.create_task(self.core_handler.get_bist(address, on_self_test_result))

    def enable_bist(self, address: str, on_result: Callable[[CommonResult], None]):
        asyncio.create_task(self.core_handler.enable_bist(address, on_result))

    def disable_bist(self, address: str, on_result: Callable[[CommonResult], None]):
        asyncio.create_task(self.core_handler.disable_bist(address, on_result))

    def set_bist_interval(
            self,
            address: str,
            interval: int,
            on_result: Callable[[CommonResult], None]
    ):
        asyncio.create_task(self.core_handler.set_bist_interval(address, interval, on_result))

    """ ********************************** Streaming data APIs ******************************** """

    def start_streaming_accel_data(
            self,
            address: str,
            on_accel_streaming_data: Callable[[CommonResult, Optional[AccelData], int], None] = None,
    ):
        asyncio.create_task(self.core_handler.start_streaming_accel_data(address, on_accel_streaming_data))

    def start_streaming_ecg_data(
            self,
            address: str,
            on_ecg_streaming_data: Callable[[CommonResult, Optional[EcgData], int], None] = None,
    ):
        asyncio.create_task(self.core_handler.start_streaming_ecg_data(address, on_ecg_streaming_data))

    def start_streaming_ppg_data(
            self,
            address: str,
            on_ppg_streaming_data: Callable[[CommonResult, Optional[PpgData], int], None] = None,
    ):
        asyncio.create_task(self.core_handler.start_streaming_ppg_data(address, on_ppg_streaming_data))

    def start_streaming_temp_data(
            self,
            address: str,
            on_temp_streaming_data: Callable[[CommonResult, Optional[TempData], int], None] = None,
    ):
        asyncio.create_task(self.core_handler.start_streaming_temp_data(address, on_temp_streaming_data))

    def stop_streaming_data(
            self,
            address: str,
            sensor_type: SensorType,
            on_result: Callable[[CommonResult], None]
    ):
        asyncio.create_task(self.core_handler.stop_streaming_data(address, sensor_type, on_result))

    """ ********************************** Data Recording APIs ******************************** """

    def get_record_samples_threshold(
            self,
            address: str,
            on_record_samples_threshold: Callable[[CommonResult, Optional[SamplesThreshold]], None]
    ):
        asyncio.create_task(self.core_handler.get_record_samples_threshold(address, on_record_samples_threshold))

    def start_record(
            self,
            address: str,
            samples: int,
            sensor_type: SensorType,
            on_result: Callable[[CommonResult], None]
    ):
        asyncio.create_task(self.core_handler.start_record(address, samples, sensor_type, on_result))

    def stop_record(
            self,
            address: str,
            sensor_type: SensorType,
            on_result: Callable[[CommonResult], None]
    ):
        asyncio.create_task(self.core_handler.stop_record(address, sensor_type, on_result))

    def get_record(self, address: str, sensor_type: SensorType, start_index: int):
        asyncio.create_task(self.core_handler.get_record(address, sensor_type, start_index))

    def set_record_callback(self, callback: RecordDataCallback):
        self.core_handler.set_record_callback(callback)

    def remove_record_callback(self, callback: RecordDataCallback):
        self.core_handler.remove_record_callback(callback)

    """ ********************************** Device Settings APIs ******************************** """

    def get_all_settings(
            self,
            address: str,
            on_settings: Callable[[CommonResult, Optional[DeviceSettings]], None]
    ):
        asyncio.create_task(self.core_handler.get_all_settings(address, on_settings))

    def set_log_settings(
            self,
            address: str,
            settings: LogSettings,
            on_result: Callable[[CommonResult], None]
    ):
        asyncio.create_task(self.core_handler.set_log_settings(address, settings, on_result))

    """ ********************************** Sensor Settings APIs ******************************** """

    def set_ecg_settings(
            self,
            address: str,
            settings: EcgSettings,
            on_result: Callable[[CommonResult], None]
    ):
        asyncio.create_task(self.core_handler.set_ecg_settings(address, settings, on_result))

    def set_ppg_settings(
            self,
            address: str,
            settings: PpgSettings,
            on_result: Callable[[CommonResult], None]
    ):
        asyncio.create_task(self.core_handler.set_ppg_settings(address, settings, on_result))

    def set_accel_settings(
            self,
            address: str,
            settings: AccelSettings,
            on_result: Callable[[CommonResult], None]
    ):
        asyncio.create_task(self.core_handler.set_accel_settings(address, settings, on_result))

    """ ********************************** Firmware Update APIs ******************************** """

    def update_firmware(self, address: str, dfu_path: str, on_result: Callable[[CommonResult], None]):
        asyncio.create_task(self.core_handler.update_firmware(address, dfu_path, on_result))

    """ ********************************** Power Management APIs ******************************** """

    def set_sleep_time(self, address: str, seconds: int, on_result: Callable[[CommonResult], None]):
        asyncio.create_task(self.core_handler.set_sleep_time(address, seconds, on_result))

    """ ********************************** Time Syncing APIs ******************************** """

    def set_time_sync(self, address: str, epoch: int, on_result: Callable[[CommonResult], None]):
        asyncio.create_task(self.core_handler.set_time_sync(address, epoch, on_result))

    def get_time_sync(self, address: str, on_time_sync: Callable[[CommonResult, Optional[int]], None]):
        asyncio.create_task(self.core_handler.get_time_sync(address, on_time_sync))

    """ ********************************** General APIs ******************************** """

    def get_device_info(
            self,
            address: str,
            on_device_info: Callable[[CommonResult, Optional[DeviceInfo]], None]
    ):
        asyncio.create_task(self.core_handler.get_device_info(address, on_device_info))

    def get_device_status(
            self,
            address: str,
            on_device_status: Callable[[CommonResult, Optional[DeviceStatus]], None]
    ):
        asyncio.create_task(self.core_handler.get_device_status(address, on_device_status))

    def get_protocol_info(
            self,
            address: str,
            on_protocol_info: Callable[[CommonResult, Optional[Protocol]], None]
    ):
        asyncio.create_task(self.core_handler.get_protocol_info(address, on_protocol_info))

    """ ********************************** Reset APIs ******************************** """

    def factory_reset(self, address: str, on_result: Callable[[CommonResult], None]):
        asyncio.create_task(self.core_handler.factory_reset(address, on_result))

    def reboot(self, address: str, on_result: Callable[[CommonResult], None]):
        asyncio.create_task(self.core_handler.reboot(address, on_result))
