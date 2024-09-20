from ble.old_ble_manager import OldBleManager
from core.models import EcgData, PpgData
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from typing import List, Tuple, Callable
from bleak import BleakClient
import asyncio

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton

class QTGuideWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Test Bioring SDK")
        self.setMinimumSize(400,400)
        parentLayout = QVBoxLayout()
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

        parentLayout.addWidget(self.label1)
        parentLayout.addWidget(self.scanBtn)
        parentLayout.addWidget(self.stopBtn)
        parentLayout.addWidget(self.connectBtn)
        parentLayout.addWidget(self.disconnectBtn)
        parentLayout.addWidget(self.get_bluetooth_state)
        parentLayout.addWidget(self.getInfoBtn)
        parentLayout.addWidget(self.start_live_acc)
        parentLayout.addWidget(self.stop_live_acc)
        parentLayout.addWidget(self.start_live_ecg)
        parentLayout.addWidget(self.stop_live_ecg)
        parentLayout.addWidget(self.start_live_ppg)
        parentLayout.addWidget(self.stop_live_ppg)
        parentLayout.addWidget(self.start_live_temp)
        parentLayout.addWidget(self.stop_live_temp)
        

        centerWidget = QWidget()
        centerWidget.setLayout(parentLayout)
        self.setCentralWidget(centerWidget)
        