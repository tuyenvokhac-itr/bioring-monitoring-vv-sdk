from abc import ABC, abstractmethod
from bleak import BleakClient

from core.models.device_info import DeviceInfo
from core.models.raw_data.accel_data import AccelData


class CoreHandlerCallBack(ABC):
    # Listener - BLE
    @abstractmethod
    def on_device_found(self):
        pass

    @abstractmethod
    def on_device_connected(self, device: BleakClient):
        pass

    @abstractmethod
    def on_device_disconnected(self, device: BleakClient):
        pass

    # Listener - Device Info
    @abstractmethod
    def on_device_info_received(self, device_info: DeviceInfo):
        pass

    @abstractmethod
    def on_charging_info_received(self, charging: bool):
        pass

    @abstractmethod
    def on_battery_level_received(self, battery_level: int):
        pass

    @abstractmethod
    def on_hr_received(self, hr: int):
        pass

    @abstractmethod
    def on_spo2_received(self, spo2: int):
        pass

    # Listener - Data

    @abstractmethod
    def on_acc_data_received(self, acc: AccelData):
        pass

    @abstractmethod
    def on_ecg_data_received(self):
        pass

    @abstractmethod
    def on_ppg_data_received(self):
        pass

    @abstractmethod
    def on_temp_data_received(self, _sender, temp):
        pass
