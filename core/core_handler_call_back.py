from abc import ABC, abstractmethod
from bleak import BleakClient

from core.models.device_info import DeviceInfo
from core.models.acc_data import AccData

class CoreHandlerCallBack(ABC):
    # Listener - BLE
    @abstractmethod
    def on_device_found():
        pass
    
    @abstractmethod
    def on_device_connected(device: BleakClient):
        pass
    
    @abstractmethod
    def on_device_disconnected(device: BleakClient):
        pass
    
    # Listener - Device Info
    @abstractmethod
    def on_device_info_received(device_info: DeviceInfo):
        pass
    
    # Listener - Data
    
    @abstractmethod
    def on_acc_data_received(acc : AccData):
        pass
    
    @abstractmethod
    def on_ecg_data_received():
        pass
    
    @abstractmethod
    def on_ppg_data_received():
        pass
    
    @abstractmethod
    def on_temp_data_received(_sender, temp):
        pass