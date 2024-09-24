from abc import ABC, abstractmethod

from ble.bt_device import BTDevice
from core.enum.general_enum import SensorType
from core.models import AccelData, EcgData, PpgData, TempData
from errors.common_error import CommonError


class RecordDataCallback(ABC):
    @abstractmethod
    def on_record_finished(self, device: BTDevice, sensor_type: SensorType):
        pass

    @abstractmethod
    def on_accel_recorded(self, device: BTDevice, data: AccelData):
        pass

    @abstractmethod
    def on_ecg_received(self, device: BTDevice, data: EcgData):
        pass

    @abstractmethod
    def on_ppg_received(self, device: BTDevice, data: PpgData):
        pass

    @abstractmethod
    def on_temp_received(self, device: BTDevice, data: TempData):
        pass

    @abstractmethod
    def on_record_error(self, device: BTDevice, data: CommonError):
        pass