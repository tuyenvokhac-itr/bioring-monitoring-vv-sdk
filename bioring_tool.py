from PyQt6.QtWidgets import QApplication
from qt_gui import QTGuideWindow
from core.core_handler import CoreHandler
from core.core_handler_call_back import CoreHandlerCallBack
from bleak import BleakClient

class BioRingTool(CoreHandlerCallBack):
    def __init__(self):
        self.core_handler = CoreHandler(self)
        app = QApplication([])
        window = QTGuideWindow()
        window.scanBtn.clicked.connect(self.start_scan)
        window.connectBtn.clicked.connect(self.connect)
        
        window.show()
        app.exec()
        
    def is_bluetooth_enabled(self):
        pass

    def start_scan(self):
        self.core_handler.start_scan()

    def stop_scan(self):
        pass

    def connect(self):
        self.core_handler.connect()

    def disconnect(self):
        pass

    # Command functions - Device info

    def get_device_info(self):
        pass

    # Command functions - Data

    def live_acc_data(self):
        pass

    def live_ecg_data(self):
        pass

    def live_ppg_data(self):
        pass

    def live_temp_data(self):
        pass
        
    # Listener - BLE

    def on_device_found(self):
        pass

    def on_device_connected(self, device: BleakClient):
        print('connected thoi')

    def on_device_disconnected(self):
        pass

    # Listener - Device Info

    def on_device_info_received(self):
        pass

    # Listener - Data

    def on_acc_data_received(self):
        pass

    def on_ecg_data_received(self):
        pass

    def on_ppg_data_received(self):
        pass

    def on_temp_data_received(self):
        pass