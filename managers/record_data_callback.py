from abc import ABC, abstractmethod

from ble.bt_device import BTDevice
from core.enum.sensor_type import SensorType
from core.models.raw_data.accel_data import AccelData
from core.models.raw_data.ecg_data import EcgData
from core.models.raw_data.ppg_data import PpgData
from core.models.raw_data.temp_data import TempData
from errors.common_error import CommonError


class RecordDataCallback(ABC):
    @abstractmethod
    def on_record_finished(self, device: BTDevice, sensor_type: SensorType):
        pass

    @abstractmethod
    def on_accel_recorded(self, device: BTDevice, data: AccelData):
        pass

    @abstractmethod
    def on_ecg_recorded(self, device: BTDevice, data: EcgData):
        pass

    @abstractmethod
    def on_ppg_recorded(self, device: BTDevice, data: PpgData):
        pass

    @abstractmethod
    def on_temp_recorded(self, device: BTDevice, data: TempData):
        pass

    @abstractmethod
    def on_record_error(self, device: BTDevice, data: CommonError):
        pass