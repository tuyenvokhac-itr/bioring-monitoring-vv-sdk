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

    @abstractmethod
    def start_scan(self):
        """
        Start scanning for Bluetooth devices.
        Device satisfies the condition will be returned in BluetoothCallback.on_scan_result.
        Currently, we scan by service UUID in BleConstant (BleConstant.BRS_UUID_SERVICE).
        Refer to BluetoothCallback for more information.
        """
        pass

    @abstractmethod
    def stop_scan(self):
        """
        Stop scanning for Bluetooth devices.
        """
        pass

    @abstractmethod
    def connect(self, address: str, timeout: int):
        """
        Connect to the Bluetooth device with the given address.
        If the connection is successful, BluetoothCallback.on_device_connected will be called.
        If the connection is unsuccessful, BluetoothCallback.on_bluetooth_error will be called.
        Refer to BluetoothCallback for more information.

        Args:
            address: Bluetooth address of the device to connect to.
        """
        pass

    @abstractmethod
    def disconnect(self, address: str):
        """
        Disconnect from the Bluetooth device with the given address.
        If the device is disconnected, BluetoothCallback.on_bluetooth_error will be called with an error: DEVICE_DISCONNECTED.

        Args:
            address: Bluetooth address of the device to disconnect from.
        """
        pass

    @abstractmethod
    def get_bluetooth_state(self) -> bool:
        """
        Check the current state of Bluetooth.
        Returns True if Bluetooth is on, False otherwise.
        """
        pass

    @abstractmethod
    def set_bluetooth_callback(self, callback: BluetoothCallback):
        """
        Set BluetoothCallback to listen to Bluetooth events.
        Class desired to listen to Bluetooth events should implement BluetoothCallback interface.
        Refer to BluetoothCallback for more information.

        Args:
            callback: BluetoothCallback to listen to Bluetooth events.
        """
        pass

    """ ********************************** Bluetooth Settings APIs ******************************** """

    @abstractmethod
    def set_bluetooth_settings(
            self,
            address: str,
            settings: BTSettings,
            on_result: Callable[[CommonResult], None],
    ):
        """
        Set Bluetooth settings to the device with the given address.

        Args:
            address: Bluetooth address of the device to set settings.
            settings: BTSettings object containing the settings to set.
            on_result: Callback to be called when result of setting Bluetooth settings is received.
        """
        pass

    """ ********************************** Self Test APIs ******************************** """

    @abstractmethod
    def get_post(
            self,
            address: str,
            on_self_test_result: Callable[[CommonResult, Optional[SelfTestResult]], None]
    ):
        """
        Get POST (Power On Self Test) result from the device with the given address.

        Args:
            address: Bluetooth address of the device to get POST result.
            on_self_test_result: Callback to be called when the POST result is received.
        """
        pass

    @abstractmethod
    def get_bist(
            self,
            address: str,
            on_self_test_result: Callable[[CommonResult, Optional[SelfTestResult]], None]
    ):
        """
        Get BIST (Built-In Self Test) result from the device with the given address.

        Args:
            address: Bluetooth address of the device to get BIST result.
            on_self_test_result: Callback to be called when the BIST result is received.
        """
        pass

    @abstractmethod
    def enable_bist(self, address: str, on_result: Callable[[CommonResult], None]):
        """
        Enable BIST (Built-In Self Test) on the device with the given address.

        Args:
            address: Bluetooth address of the device to enable BIST.
            on_result: Callback to be called when result of enabling BIST is received.
        """
        pass

    @abstractmethod
    def disable_bist(self, address: str, on_result: Callable[[CommonResult], None]):
        """
        Disable BIST (Built-In Self Test) on the device with the given address.

        Args:
            address: Bluetooth address of the device to disable BIST.
            on_result: Callback to be called when result of disabling BIST is received.
        """
        pass

    @abstractmethod
    def set_bist_interval(
            self,
            address: str,
            interval: int,
            on_result: Callable[[CommonResult], None]
    ):
        """
        Set BIST (Built-In Self Test) interval on the device with the given address.

        Args:
            address: Bluetooth address of the device to set BIST interval.
            interval: Interval in seconds to set for BIST.
            on_result: Callback to be called when result of setting BIST interval is received.
        """
        pass

    """ ********************************** Streaming data APIs ******************************** """

    @abstractmethod
    def start_streaming_accel_data(
            self,
            address: str,
            on_accel_streaming_data: Callable[[CommonResult, Optional[AccelData], int], None] = None,
    ):
        """
        Start streaming accelerometer data from the device with the given address.
        If the streaming is successful, on_accel_streaming_data will be called with successful CommonResult, AccelData and packet lost.
        If there is error in one sample, on_accel_streaming_data will be called with the error on CommonResult.

        Args:
            address: Bluetooth address of the device to start streaming accelerometer data.
            on_accel_streaming_data: Callback to be called when accelerometer data is received: result, Accel data, packet lost.
        """
        pass

    @abstractmethod
    def start_streaming_ecg_data(
            self,
            address: str,
            on_ecg_streaming_data: Callable[[CommonResult, Optional[EcgData], int], None] = None,
    ):
        """
        Start streaming ECG data from the device with the given address.
        If the streaming is successful, on_ecg_streaming_data will be called with successful CommonResult, EcgData and packet lost.
        If there is error in one sample, on_ecg_streaming_data will be called with the error on CommonResult.

        Args:
            address: Bluetooth address of the device to start streaming ECG data.
            on_ecg_streaming_data: Callback to be called when ECG data is received: result, Ecg data, packet lost.
        """
        pass

    @abstractmethod
    def start_streaming_ppg_data(
            self,
            address: str,
            on_ppg_streaming_data: Callable[[CommonResult, Optional[PpgData], int], None] = None,
    ):
        """
        Start streaming PPG data from the device with the given address.
        If the streaming is successful, on_ppg_streaming_data will be called with successful CommonResult, PpgData and packet lost.
        If there is error in one sample, on_ppg_streaming_data will be called with the error on CommonResult.

        Args:
            address: Bluetooth address of the device to start streaming PPG data.
            on_ppg_streaming_data: Callback to be called when PPG data is received: result, Ppg data, packet lost.
        """
        pass

    @abstractmethod
    def start_streaming_temp_data(
            self,
            address: str,
            on_temp_streaming_data: Callable[[CommonResult, Optional[TempData], int], None] = None,
    ):
        """
        Start streaming temperature data from the device with the given address.
        If the streaming is successful, on_temp_streaming_data will be called with successful CommonResult, TempData and packet lost.
        If there is error in one sample, on_temp_streaming_data will be called with the error on CommonResult.

        Args:
            address: Bluetooth address of the device to start streaming temperature data.
            on_temp_streaming_data: Callback to be called when temperature data is received: result, Temp data, packet lost.
        """
        pass

    @abstractmethod
    def stop_streaming_data(
            self,
            address: str,
            sensor_type: SensorType,
            on_result: Callable[[CommonResult], None]
    ):
        """
        Stop streaming data from the device with the given address.
        
        Args:
            address: Bluetooth address of the device to stop streaming data.
            sensor_type: SensorType of the data to stop streaming.
            on_result: Callback to be called when result of stopping streaming data is received.
        """
        pass

    """ ********************************** Data Recording APIs ******************************** """

    @abstractmethod
    def get_record_samples_threshold(
            self,
            address: str,
            on_record_samples_threshold: Callable[[CommonResult, Optional[SamplesThreshold]], None]
    ):
        """
        Get record samples threshold from the device with the given address.
        If the record samples threshold is successfully received, on_record_samples_threshold will be called with successful CommonResult and SamplesThreshold.
        
        Args:
            address: Bluetooth address of the device to get record samples threshold.
            on_record_samples_threshold: Callback to be called when result of samples threshold is received.
        """
        pass

    @abstractmethod
    def start_record(
            self,
            address: str,
            samples: int,
            sensor_type: SensorType,
            on_result: Callable[[CommonResult], None]
    ):
        """
        Start recording data from the device with the given address.
        When a record is finished, RecordDataCallback.on_record_finished will be called.
        After that, the recorded data can be retrieved using get_record.

        Args:
            address: Bluetooth address of the device to start recording data.
            samples: Number of samples to record.
            sensor_type: SensorType of the data to record.
            on_result: Callback to be called when result of starting recording data is received.
        """
        pass

    @abstractmethod
    def stop_record(
            self, address: str,
            sensor_type: SensorType,
            on_result: Callable[[CommonResult], None]
    ):
        """
        Stop recording data from the device with the given address.

        Args:
            address: Bluetooth address of the device to stop recording data.
            sensor_type: SensorType of the data to stop recording.
            on_result: Callback to be called when result of stopping recording data is received.
        """
        pass

    @abstractmethod
    def get_record(self, address: str, sensor_type: SensorType, start_index: int):
        """
        Get recorded data from the device with the given address.
        If the recorded data is successfully received, RecordDataCallback.on_accel_recorded, on_ecg_recorded, on_ppg_recorded or on_temp_recorded will be called.

        Args:
            address: Bluetooth address of the device to get recorded data.
            sensor_type: SensorType of the data to get.
            start_index: Index of the data to start getting.
        """
        pass

    @abstractmethod
    def set_record_callback(self, callback: RecordDataCallback):
        """
        Set RecordDataCallback to listen to recorded data.

        Args:
            callback: RecordDataCallback to listen to recorded data.
        """
        pass

    @abstractmethod
    def remove_record_callback(self, callback: RecordDataCallback):
        """
        Remove RecordDataCallback from listening to recorded data.

        Args:
            callback: RecordDataCallback to remove from listening to recorded data.
        """
        pass

    """ ********************************** Device Settings APIs ******************************** """

    @abstractmethod
    def get_all_settings(
            self,
            address: str,
            on_settings: Callable[[CommonResult, Optional[DeviceSettings]], None]
    ):
        """
        Get all settings from the device with the given address.

        Args:
            address: Bluetooth address of the device to get settings.
            on_settings: Callback to be called when result of getting settings is received.
        """
        pass

    @abstractmethod
    def set_log_settings(
            self,
            address: str,
            settings: LogSettings,
            on_result: Callable[[CommonResult], None]
    ):
        """
        Set log settings to the device with the given address.

        Args:
            address: Bluetooth address of the device to set log settings.
            settings: LogSettings object containing the settings to set.
            on_result: Callback to be called when result of setting log settings is received.
        """
        pass

    """ ********************************** Sensor Settings APIs ******************************** """

    @abstractmethod
    def set_ecg_settings(
            self,
            address: str,
            settings: EcgSettings,
            on_result: Callable[[CommonResult], None]
    ):
        """
        Set ECG settings to the device with the given address.

        Args:
            address: Bluetooth address of the device to set ECG settings.
            settings: EcgSettings object containing the settings to set.
            on_result: Callback to be called when result of setting ECG settings is received.
        """
        pass

    @abstractmethod
    def set_ppg_settings(
            self,
            address: str,
            settings: PpgSettings,
            on_result: Callable[[CommonResult], None]
    ):
        """
        Set PPG settings to the device with the given address.

        Args:
            address: Bluetooth address of the device to set PPG settings.
            settings: PpgSettings object containing the settings to set.
            on_result: Callback to be called when result of setting PPG settings is received.
        """
        pass

    @abstractmethod
    def set_accel_settings(
            self,
            address: str,
            settings: AccelSettings,
            on_result: Callable[[CommonResult], None]
    ):
        """
        Set accelerometer settings to the device with the given address.

        Args:
            address: Bluetooth address of the device to set accelerometer settings.
            settings: AccelSettings object containing the settings to set.
            on_result: Callback to be called when result of setting accelerometer settings is received.
        """
        pass

    """ ********************************** Firmware Update APIs ******************************** """

    @abstractmethod
    def update_firmware(self, address: str, dfu_path: str, on_result: Callable[[CommonResult], None]):
        """
        Update firmware of the device with the given address.
        After update firmware successfully, the device will be disconnected and need at least 15 seconds to ready.
        All settings will be kept the same after updating firmware.

        Args:
            address: Bluetooth address of the device to update firmware.
            dfu_path: Path to the DFU file to update. (.cyacd2 file)
            on_result: Callback to be called when result of updating firmware is received.
        """
        pass

    """ ********************************** Power Management APIs ******************************** """

    @abstractmethod
    def set_sleep_time(self, address: str, seconds: int, on_result: Callable[[CommonResult], None]):
        """
        Set time out before device goes to sleep.

        Args:
            address: Bluetooth address of the device to set sleep time.
            seconds: Time in seconds before device goes to sleep.
            on_result: Callback to be called when result of setting sleep time is received.
        """
        pass

    """ ********************************** Time Syncing APIs ******************************** """

    @abstractmethod
    def set_time_sync(self, address: str, epoch: int, on_result: Callable[[CommonResult], None]):
        """
        Set time sync to the device with the given address.

        Args:
            address: Bluetooth address of the device to set time sync.
            epoch: Epoch time to set.
            on_result: Callback to be called when result of setting time sync is received.
        """
        pass

    @abstractmethod
    def get_time_sync(self, address: str, on_time_sync: Callable[[CommonResult, Optional[int]], None]):
        """
        Get time sync from the device with the given address.

        Args:
            address: Bluetooth address of the device to get time sync.
            on_time_sync: Callback to be called when result of getting time sync is received, including epoch time.
        """
        pass

    """ ********************************** General APIs ******************************** """

    @abstractmethod
    def get_device_info(
            self,
            address: str,
            on_device_info: Callable[[CommonResult, Optional[DeviceInfo]], None]
    ):
        """
        Get device information from the device with the given address.

        Args:
            address: Bluetooth address of the device to get device information.
            on_device_info: Callback to be called when result of getting device information is received.
        """
        pass

    @abstractmethod
    def get_device_status(
            self,
            address: str,
            on_device_status: Callable[[CommonResult, Optional[DeviceStatus]], None]
    ):
        """
        Get device status from the device with the given address.

        Args:
            address: Bluetooth address of the device to get device status.
            on_device_status: Callback to be called when result of getting device status is received.
        """
        pass

    @abstractmethod
    def get_protocol_info(
            self,
            address: str,
            on_protocol_info: Callable[[CommonResult, Optional[Protocol]], None]
    ):
        """
        Get protocol information from the device with the given address.

        Args:
            address: Bluetooth address of the device to get protocol information.
            on_protocol_info: Callback to be called when result of getting protocol information is received.
        """
        pass

    """ ********************************** Reset APIs ******************************** """

    @abstractmethod
    def factory_reset(self, address: str, on_result: Callable[[CommonResult], None]):
        """
        Factory reset the device with the given address.
        Currently, factory reset does not reboot device, it just reset the settings.

        Args:
            address: Bluetooth address of the device to factory reset.
            on_result: Callback to be called when result of factory reset is received.
        """
        pass

    @abstractmethod
    def reboot(self, address: str, on_result: Callable[[CommonResult], None]):
        """
        Reboot the device with the given address.

        Args:
            address: Bluetooth address of the device to reboot.
            on_result: Callback to be called when result of reboot is received.
        """
        pass
