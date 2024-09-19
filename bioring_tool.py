from PyQt6.QtWidgets import QApplication

from ble.bt_device import BTDevice
from errors.common_error import CommonError
from managers.bluetooth_callback import BluetoothCallback
from managers.ring_manager import RingManager
from qt_gui import QTGuideWindow
from core.core_handler import CoreHandler
from bleak import BleakClient
from core.core_handler_call_back import CoreHandlerCallBack
from ble.ble_constant import BleConstant
from core.command import (
    GetDeviceInfoCommand,
    LiveAccDataCommand,
    LiveEcgDataCommand,
    LivePpgDataCommand,
    LiveTempDataCommand,
)
from core.models.device_info import DeviceInfo
from core.models.acc_data import AccData
from qasync import QEventLoop 
import asyncio


class BioRingTool(CoreHandlerCallBack, BluetoothCallback):
    def __init__(self):
        self.core_handler = CoreHandler(self)
        self.ring_manager = RingManager()

        app = QApplication([])
        loop = QEventLoop(app)
        asyncio.set_event_loop(loop)

        window = QTGuideWindow()
        window.scanBtn.clicked.connect(self.start_scan)
        window.connectBtn.clicked.connect(self.connect)
        window.disconnectBtn.clicked.connect(self.disconnect)
        window.getInfoBtn.clicked.connect(self.get_device_info)
        window.start_live_acc.clicked.connect(self.start_live_acc_data)
        window.stop_live_acc.clicked.connect(self.stop_live_acc_data)
        window.start_live_ecg.clicked.connect(self.start_live_ecg_data)
        window.stop_live_ecg.clicked.connect(self.stop_live_ecg_data)
        window.start_live_ppg.clicked.connect(self.start_live_ppg_data)
        window.stop_live_ppg.clicked.connect(self.stop_live_ppg_data)
        window.start_live_temp.clicked.connect(self.start_live_temp_data)
        window.stop_live_temp.clicked.connect(self.stop_live_temp_data)


        window.show()
        # Run the PyQt event loop alongside asyncio
        with loop:
            loop.run_forever()

    """ Implement BluetoothCallback """
    def on_scan_result(self, device: BTDevice):
        pass

    def on_device_connected(self, device: BleakClient):
        # self.core_handler.start_notify()
        pass

    def on_bluetooth_error(self, error: CommonError):
        pass

    def on_bluetooth_state_changed(self, status: bool):
        pass





    def is_bluetooth_enabled(self):
        pass

    def start_scan(self):
        # self.core_handler.start_scan()
        self.ring_manager.start_scan()

    def stop_scan(self):
        pass

    def connect(self):
        # self.core_handler.connect()
        print('test not block')

    def disconnect(self):
        self.core_handler.disconnect()

    # Command functions - Device info

    def get_device_info(self):
        self.core_handler.get_device_info()

    # Command functions - Data

    def start_live_acc_data(self):
        self.core_handler.live_acc_data()

    def stop_live_acc_data(self):
        self.core_handler.live_acc_data(isStart=False)

    def start_live_ecg_data(self):
        self.core_handler.live_ecg_data()

    def stop_live_ecg_data(self):
        self.core_handler.live_ecg_data(isStart=False)

    def start_live_ppg_data(self):
        self.core_handler.live_ppg_data()

    def stop_live_ppg_data(self):
        self.core_handler.live_ppg_data(isStart=False)

    def start_live_temp_data(self):
        self.core_handler.live_temp_data()

    def stop_live_temp_data(self):
        print("stop live temp data")
        # self.core_handler.live_temp_data(isStart=False)

    # Listener - BLE

    def on_device_found(self):
        pass

    # def on_device_connected(self, device: BleakClient):
    #     # self.core_handler.start_notify()
    #     pass

    def on_device_disconnected(self):
        pass

    # Listener - Device Info

    def on_device_info_received(self, device: DeviceInfo):
        print(device)

    def on_charging_info_received(self, charging: bool):
        print(f"[NT] Charging status: {charging}")

    def on_battery_level_received(self, battery_level: int):
        print(f"[NT] Battery level: {battery_level}")

    def on_hr_received(self, hr: int):
        print(f"[NT] HR: {hr}")

    def on_spo2_received(self, spo2: int):
        print(f"[NT] SpO2: {spo2}")

    # Listener - Data

    def on_acc_data_received(self, acc: AccData):
        print(acc)

    def on_ecg_data_received(self):
        pass

    def on_ppg_data_received(self):
        pass

    def on_temp_data_received(self, temp):
        print(f"[NT] Temperature: {temp}")
