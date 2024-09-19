from abc import ABC, abstractmethod

from ble.bt_device import BTDevice
from errors.common_error import CommonError


class BluetoothCallback(ABC):
    @abstractmethod
    def on_scan_result(self, device: BTDevice):
        pass

    @abstractmethod
    def on_device_connected(self, device: BTDevice):
        pass

    @abstractmethod
    def on_bluetooth_error(self, error: CommonError):
        pass

    @abstractmethod
    def on_bluetooth_state_changed(self, status: bool):
        pass