import sys
from typing import List, Optional

from PyQt6.QtWidgets import QApplication

from ble.bt_device import BTDevice
from errors.common_error import CommonError
from errors.common_result import CommonResult
from managers.bluetooth_callback import BluetoothCallback
from managers.ring_manager import RingManager
from qt_gui import QTGuideWindow
from bleak import BleakClient
from core.core_handler_call_back import CoreHandlerCallBack
from core.models.device_info import DeviceInfo
from core.models.raw_data.accel_data import AccelData
from qasync import QEventLoop
import asyncio


class BioRingTool(CoreHandlerCallBack, BluetoothCallback):
    def __init__(self):
        self.ring_manager = RingManager()
        self.ring_manager.set_bluetooth_callback(self)
        self.devices : List[BTDevice] = []

        app = QApplication([])
        loop = QEventLoop(app)
        asyncio.set_event_loop(loop)

        window = QTGuideWindow(self.close_event)
        window.scanBtn.clicked.connect(self.start_scan)
        window.stopBtn.clicked.connect(self.stop_scan)
        window.connectBtn.clicked.connect(self.connect)
        window.disconnectBtn.clicked.connect(self.disconnect)
        window.get_bluetooth_state.clicked.connect(self.get_bluetooth_state)
        window.getInfoBtn.clicked.connect(self.get_device_info)
        window.start_live_acc.clicked.connect(self.start_live_acc_data)
        window.stop_live_acc.clicked.connect(self.stop_live_acc_data)
        window.start_live_ecg.clicked.connect(self.start_live_ecg_data)
        window.stop_live_ecg.clicked.connect(self.stop_live_ecg_data)
        window.start_live_ppg.clicked.connect(self.start_live_ppg_data)
        window.stop_live_ppg.clicked.connect(self.stop_live_ppg_data)
        window.start_live_temp.clicked.connect(self.start_live_temp_data)
        window.stop_live_temp.clicked.connect(self.stop_live_temp_data)

        # # Create the Bluetooth state receiver
        # self.bt_receiver = BluetoothStateReceiver()
        # self.bt_receiver.bluetoothStateChanged.connect(self.handle_bluetooth_state_change)
        #
        # # Start the Bluetooth listener thread
        # self.bt_listener_thread = BluetoothListenerThread(self.bt_receiver.bluetoothStateChanged.emit)
        # self.bt_listener_thread.start()

        window.show()
        # Run the PyQt event loop alongside asyncio
        with loop:
            loop.run_forever()

    def close_event(self):
        # Stop the Bluetooth listener thread when closing the application
        print('close event')
        # self.bt_listener_thread.stop()
        # self.bt_listener_thread.join()

    def handle_bluetooth_state_change(self, state: str):
        print(f"Bluetooth state changed: {state}")


    """ BLE actions"""

    def start_scan(self):
        self.ring_manager.start_scan()

    def stop_scan(self):
        self.ring_manager.stop_scan()

    def connect(self):
        self.ring_manager.connect(self.devices[0].address, 10)
        print('connect to device', self.devices[0])

    def disconnect(self,  address: str):
        self.ring_manager.disconnect(self.devices[0].address)

    def get_bluetooth_state(self):
        state = self.ring_manager.get_bluetooth_state()
        print(state)

    """ BluetoothCallback """

    def on_scan_result(self, device: BTDevice):
        print(f"on_scan_result Device found: {device}")
        self.devices.append(device)

    def on_device_connected(self, device: BleakClient):
        print(f"on_device_connected Device connected: {device}")

    def on_bluetooth_error(self, device: BTDevice, error: CommonError):
        print(f"on_bluetooth_error Error: {error}")

    def on_bluetooth_state_changed(self, status: bool):
        pass

    # Command functions - Device info

    def get_device_info(self):
        self.ring_manager.get_device_info(self.devices[0].address, self.on_device_info)

    def on_device_info(self, result: CommonResult, info: Optional[DeviceInfo]):
        print(f"on_device_info Result: {result}")
        print(f"on_device_info Device info: {info}")

    # Command functions - Data

    def start_live_acc_data(self):
        pass

    def stop_live_acc_data(self):
        pass

    def start_live_ecg_data(self):
        pass

    def stop_live_ecg_data(self):
        pass

    def start_live_ppg_data(self):
        pass

    def stop_live_ppg_data(self):
        pass

    def start_live_temp_data(self):
        pass

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

    def on_acc_data_received(self, acc: AccelData):
        print(acc)

    def on_ecg_data_received(self):
        pass

    def on_ppg_data_received(self):
        pass

    def on_temp_data_received(self, temp):
        print(f"[NT] Temperature: {temp}")
