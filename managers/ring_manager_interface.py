from abc import ABC, abstractmethod

from managers.bluetooth_callback import BluetoothCallback


class RingManagerInterface(ABC):
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