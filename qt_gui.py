from typing import Callable

from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton


class QTGuideWindow(QMainWindow):
    def __init__(self, close_event: Callable):
        super().__init__()

        self.close_event = close_event

        self.setWindowTitle("Test Bioring SDK")
        self.setMinimumSize(400,400)
        parent_layout = QVBoxLayout()
        self.label1 = QLabel("Welcome to the test tool")
        self.scanBtn = QPushButton("Start Scan BLE")
        self.stopBtn = QPushButton("Stop Scan BLE")
        self.connectBtn = QPushButton("Connect")
        self.disconnectBtn = QPushButton("Disconnect")
        self.get_bluetooth_state = QPushButton("Get Bluetooth state")
        self.getInfoBtn = QPushButton("Get tool info")
        self.start_live_acc = QPushButton("Start Live ACC")
        self.stop_live_acc = QPushButton("Stop Live ACC")
        self.start_live_ecg = QPushButton("Start Live ECG")
        self.stop_live_ecg = QPushButton("Stop Live ECG")
        self.start_live_ppg = QPushButton("Start Live PPG")
        self.stop_live_ppg = QPushButton("Stop Live PPG")
        self.start_live_temp = QPushButton("Start Live temp")
        self.stop_live_temp = QPushButton("Stop Live temp")

        parent_layout.addWidget(self.label1)
        parent_layout.addWidget(self.scanBtn)
        parent_layout.addWidget(self.stopBtn)
        parent_layout.addWidget(self.connectBtn)
        parent_layout.addWidget(self.disconnectBtn)
        parent_layout.addWidget(self.get_bluetooth_state)
        parent_layout.addWidget(self.getInfoBtn)
        parent_layout.addWidget(self.start_live_acc)
        parent_layout.addWidget(self.stop_live_acc)
        parent_layout.addWidget(self.start_live_ecg)
        parent_layout.addWidget(self.stop_live_ecg)
        parent_layout.addWidget(self.start_live_ppg)
        parent_layout.addWidget(self.stop_live_ppg)
        parent_layout.addWidget(self.start_live_temp)
        parent_layout.addWidget(self.stop_live_temp)
        

        center_widget = QWidget()
        center_widget.setLayout(parent_layout)
        self.setCentralWidget(center_widget)

    def closeEvent(self, event):
        self.close_event()
        super().closeEvent(event)