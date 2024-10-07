import asyncio
from typing import List, Optional

from PyQt6.QtWidgets import QApplication
from bleak import BleakClient
from qasync import QEventLoop

from ble.bt_device import BTDevice
from core.enum.sensor_type import SensorType
from core.models.device_info import DeviceInfo
from core.models.raw_data.accel_data import AccelData
from core.models.raw_data.ecg_data import EcgData
from core.models.raw_data.ppg_data import PpgData
from core.models.raw_data.samples_threshold import SamplesThreshold
from core.models.raw_data.temp_data import TempData
from core.models.self_tests.self_test_result import SelfTestResult
from core.models.settings.device_settings import DeviceSettings
from errors.common_error import CommonError
from errors.common_result import CommonResult
from managers import ring_factory as factory
from managers.bluetooth_callback import BluetoothCallback
from managers.record_data_callback import RecordDataCallback
from qt_gui import QTGuideWindow


class BioRingTool(BluetoothCallback, RecordDataCallback):
    def __init__(self):
        self.ring_manager = factory.get_ring_manager_instance()
        self.ring_manager.set_bluetooth_callback(self)
        self.ring_manager.set_record_callback(self)
        self.devices: List[BTDevice] = []

        app = QApplication([])
        loop = QEventLoop(app)
        asyncio.set_event_loop(loop)

        window = QTGuideWindow(self.close_event)
        window.scanBtn.clicked.connect(self.start_scan)
        window.stopBtn.clicked.connect(self.stop_scan)
        window.connectBtn.clicked.connect(self.connect)
        window.disconnectBtn.clicked.connect(self.disconnect)
        window.get_bluetooth_state.clicked.connect(self.get_bluetooth_state)

        window.get_post.clicked.connect(self.get_post)
        window.get_bist.clicked.connect(self.get_bist)
        window.enable_bist.clicked.connect(self.enable_bist)
        window.disable_bist.clicked.connect(self.disable_bist)
        window.set_bist_interval.clicked.connect(self.set_bist_interval)

        window.start_record.clicked.connect(self.start_record)
        window.stop_record.clicked.connect(self.stop_record)
        window.get_record_sample.clicked.connect(self.get_record_samples_threshold)
        window.get_record.clicked.connect(self.get_record)

        window.get_all_settings.clicked.connect(self.get_all_settings)

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

    def disconnect(self, address: str):
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

    # Self test
    def get_post(self):
        self.ring_manager.get_post(self.devices[0].address, self.on_post_result)

    def on_post_result(self, result: CommonResult, post: Optional[SelfTestResult]):
        print(f"on_post_result Result: {result}")

    def get_bist(self):
        self.ring_manager.get_bist(self.devices[0].address, self.on_bist_result)

    def on_bist_result(self, result: CommonResult, bist: Optional[SelfTestResult]):
        print(f"on_bist_result Result: {result}")

    def enable_bist(self):
        self.ring_manager.enable_bist(self.devices[0].address, self.on_enable_bist_result)

    def on_enable_bist_result(self, result: CommonResult):
        print(f"on_enable_bist_result Result: {result}")

    def disable_bist(self):
        self.ring_manager.disable_bist(self.devices[0].address, self.on_disable_bist_result)

    def on_disable_bist_result(self, result: CommonResult):
        print(f"on_disable_bist_result Result: {result}")

    def set_bist_interval(self, interval: int):
        self.ring_manager.set_bist_interval(self.devices[0].address, 60, self.on_set_bist_interval_result)

    def on_set_bist_interval_result(self, result: CommonResult):
        print(f"on_set_bist_interval_result Result: {result}")


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
        self.ring_manager.start_streaming_ecg_data(self.devices[0].address, self.on_ecg_data_received)

    def on_ecg_data_received(self, result: CommonResult, data: Optional[EcgData], packet_lost: int):
        print(f"on_ecg_data_received Result: {result}")
        print(f"on_ecg_data_received Data: {data}")

    def stop_live_ecg_data(self):
        self.ring_manager.stop_streaming_data(self.devices[0].address, SensorType.ECG, self.on_stop_ecg_success)

    def on_stop_ecg_success(self, result: CommonResult):
        print(f"on_stop_ecg_success Result: {result}")

    def start_live_ppg_data(self):
        self.ring_manager.start_streaming_ppg_data(self.devices[0].address, self.on_ppg_data_received)

    def on_ppg_data_received(self, result: CommonResult, data: Optional[PpgData], packet_lost: int):
        print(f"on_ppg_data_received Result: {result}")
        print(f"on_ppg_data_received Data: {data}")

    def stop_live_ppg_data(self):
        self.ring_manager.stop_streaming_data(self.devices[0].address, SensorType.PPG, self.on_stop_ppg_success)

    def on_stop_ppg_success(self, result: CommonResult):
        print(f"on_stop_ppg_success Result: {result}")

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

    def on_temp_data_received(self, temp):
        print(f"[NT] Temperature: {temp}")

    def on_record_finished(self, device: BTDevice, sensor_type: SensorType):
        print(f"[NT] Record finished: {sensor_type}, device: {device}")

    def on_accel_recorded(self, device: BTDevice, data: AccelData):
        print(f'device: {device}, data: {data}')

    def on_ecg_recorded(self, device: BTDevice, data: EcgData):
        print(f'device: {device}, data: {data}')

    def on_ppg_recorded(self, device: BTDevice, data: PpgData):
        print(f'device: {device}, data: {data}')

    def on_temp_recorded(self, device: BTDevice, data: TempData):
        print(f'device: {device}, data: {data}')

    def on_record_error(self, device: BTDevice, data: CommonError):
        print(f'device: {device}, data: {data}')

    def start_record(self):
        self.ring_manager.start_record(self.devices[0].address, 3000, SensorType.ECG, self.on_start_record_success)

    def on_start_record_success(self, result: CommonResult):
        print(f"on_record_success Result: {result}")

    def stop_record(self):
        self.ring_manager.stop_record(self.devices[0].address, SensorType.ECG, self.on_stop_record_success)

    def on_stop_record_success(self, result: CommonResult):
        print(f"on_stop_record_success Result: {result}")

    def get_record(self):
        self.ring_manager.get_record(self.devices[0].address, SensorType.ECG, 288)

    def on_get_record_success(self, result: CommonResult):
        print(f"on_get_record_success Result: {result}")

    def get_record_samples_threshold(self):
        self.ring_manager.get_record_samples_threshold(self.devices[0].address, self.on_get_record_samples_threshold)

    def on_get_record_samples_threshold(self, result: CommonResult, samples_threshold: Optional[SamplesThreshold]):
        print(f"on_get_record_samples_threshold Result: {result}")
        print(f"on_get_record_samples_threshold Samples threshold: {samples_threshold}")


    def get_all_settings(self):
        self.ring_manager.get_all_settings(self.devices[0].address, self.on_all_settings_received)

    def on_all_settings_received(self, result: CommonResult, settings: Optional[DeviceSettings]):
        print(f"on_all_settings_received Result: {result}")
        print(f"on_all_settings_received Settings: {settings}")