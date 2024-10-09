from typing import Callable

from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton


class QTGuideWindow(QMainWindow):
    def __init__(self, close_event: Callable):
        super().__init__()

        self.close_event = close_event

        self.setWindowTitle("Test Bioring SDK")
        self.setMinimumSize(800,1000)
        parent_layout = QVBoxLayout()
        self.label1 = QLabel("Welcome to the test tool")
        self.scanBtn = QPushButton("Start Scan BLE")
        self.stopBtn = QPushButton("Stop Scan BLE")
        self.connectBtn = QPushButton("Connect")
        self.disconnectBtn = QPushButton("Disconnect")
        self.get_bluetooth_state = QPushButton("Get Bluetooth state")
        self.set_bluetooth_settings = QPushButton("Set Bluetooth settings")

        self.get_post = QPushButton("Get post")
        self.get_bist = QPushButton("Get bist")
        self.enable_bist = QPushButton("Enable bist")
        self.disable_bist = QPushButton("Disable bist")
        self.set_bist_interval = QPushButton("Set bist interval")

        self.get_record_sample = QPushButton("Get record samples")
        self.start_record_ppg = QPushButton("Start record PPG")
        self.start_record_ecg = QPushButton("Start record ECG")
        self.start_record_acc = QPushButton("Start record ACC")
        self.start_record_temp = QPushButton("Start record Temp")

        self.stop_record_ecg = QPushButton("Stop record ecg")
        self.stop_record_ppg = QPushButton("Stop record ppg")
        self.stop_record_acc = QPushButton("Stop record acc")
        self.stop_record_temp = QPushButton("Stop record temp")
        self.get_record_ppg = QPushButton("Get record PPG")
        self.get_record_ecg = QPushButton("Get record ECG")
        self.get_record_acc = QPushButton("Get record ACC")
        self.get_record_temp = QPushButton("Get record Temp")

        self.get_all_settings = QPushButton("Get all settings")

        self.getInfoBtn = QPushButton("Get device info")
        self.start_live_acc = QPushButton("Start Live ACC")
        self.stop_live_acc = QPushButton("Stop Live ACC")
        self.start_live_ecg = QPushButton("Start Live ECG")
        self.stop_live_ecg = QPushButton("Stop Live ECG")
        self.start_live_ppg = QPushButton("Start Live PPG")
        self.stop_live_ppg = QPushButton("Stop Live PPG")
        self.start_live_temp = QPushButton("Start Live temp")
        self.stop_live_temp = QPushButton("Stop Live temp")

        self.set_ppg_settings = QPushButton("Set ppg settings")
        self.set_ecg_settings = QPushButton("Set ecg settings")
        self.set_acc_settings = QPushButton("Set acc settings")
        self.set_time_sync = QPushButton("Set time sync")
        self.get_time_sync = QPushButton("Get time sync")
        self.set_log_settings = QPushButton("Set log settings")

        self.set_sleep_time = QPushButton("Set sleep time")
        self.get_device_status = QPushButton("Get device status")
        self.get_protocol_info = QPushButton("Get Protocol info")

        self.reboot = QPushButton("Reboot")
        self.factory_reset = QPushButton("Factory reset")
        self.update_firmware = QPushButton("Update firmware")

        parent_layout.addWidget(self.label1)
        parent_layout.addWidget(self.scanBtn)
        parent_layout.addWidget(self.stopBtn)
        parent_layout.addWidget(self.connectBtn)
        parent_layout.addWidget(self.disconnectBtn)
        parent_layout.addWidget(self.get_bluetooth_state)
        parent_layout.addWidget(self.set_bluetooth_settings)

        parent_layout.addWidget(self.get_post)
        parent_layout.addWidget(self.get_bist)
        parent_layout.addWidget(self.enable_bist)
        parent_layout.addWidget(self.disable_bist)
        parent_layout.addWidget(self.set_bist_interval)

        parent_layout.addWidget(self.get_record_sample)
        parent_layout.addWidget(self.start_record_ppg)
        parent_layout.addWidget(self.start_record_ecg)
        parent_layout.addWidget(self.start_record_acc)
        parent_layout.addWidget(self.start_record_temp)
        parent_layout.addWidget(self.stop_record_ecg)
        parent_layout.addWidget(self.stop_record_ppg)
        parent_layout.addWidget(self.stop_record_acc)
        parent_layout.addWidget(self.stop_record_temp)
        parent_layout.addWidget(self.get_record_ppg)
        parent_layout.addWidget(self.get_record_ecg)
        parent_layout.addWidget(self.get_record_acc)
        parent_layout.addWidget(self.get_record_temp)

        parent_layout.addWidget(self.get_all_settings)

        parent_layout.addWidget(self.getInfoBtn)
        parent_layout.addWidget(self.start_live_acc)
        parent_layout.addWidget(self.stop_live_acc)
        parent_layout.addWidget(self.start_live_ecg)
        parent_layout.addWidget(self.stop_live_ecg)
        parent_layout.addWidget(self.start_live_ppg)
        parent_layout.addWidget(self.stop_live_ppg)
        parent_layout.addWidget(self.start_live_temp)
        parent_layout.addWidget(self.stop_live_temp)

        parent_layout.addWidget(self.set_ppg_settings)
        parent_layout.addWidget(self.set_ecg_settings)
        parent_layout.addWidget(self.set_acc_settings)
        parent_layout.addWidget(self.reboot)
        parent_layout.addWidget(self.set_time_sync)
        parent_layout.addWidget(self.get_time_sync)
        parent_layout.addWidget(self.set_log_settings)

        parent_layout.addWidget(self.set_sleep_time)
        parent_layout.addWidget(self.get_device_status)
        parent_layout.addWidget(self.get_protocol_info)
        parent_layout.addWidget(self.factory_reset)
        parent_layout.addWidget(self.update_firmware)
        

        center_widget = QWidget()
        center_widget.setLayout(parent_layout)
        self.setCentralWidget(center_widget)

    def closeEvent(self, event):
        self.close_event()
        super().closeEvent(event)