from ble.ble_manager import BleManager
from core.models import EcgData, PpgData
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from typing import List, Tuple, Callable
from bleak import BleakClient

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton

class QTGuideWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tool hack Lien Minh")
        self.setMinimumSize(400,400)
        parentLayout = QVBoxLayout()
        self.label1 = QLabel("         Máy tính của bạn đã bị hack")
        self.scanBtn = QPushButton("Scan BLE")
        self.connectBtn = QPushButton("Connect")
        self.disconnectBtn = QPushButton("Disconnect")
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
        parentLayout.addWidget(self.connectBtn)
        parentLayout.addWidget(self.disconnectBtn)
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
        