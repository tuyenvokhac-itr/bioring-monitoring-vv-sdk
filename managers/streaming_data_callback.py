from abc import ABC, abstractmethod

from ble.bt_device import BTDevice
from core.models import AccelData, EcgData, PpgData, TempData


class StreamingDataCallback(ABC):
    @abstractmethod
    def on_accel_received(self, device: BTDevice, data: AccelData, packet_lost: int):
        pass

    @abstractmethod
    def on_ecg_received(self, device: BTDevice, data: EcgData, packet_lost: int):
        pass

    @abstractmethod
    def on_ppg_received(self, device: BTDevice, data: PpgData, packet_lost: int):
        pass

    @abstractmethod
    def on_temp_received(self, device: BTDevice, data: TempData, packet_lost: int):
        pass