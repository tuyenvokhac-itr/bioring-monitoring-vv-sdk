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
        self.label1 = QLabel("         Yêu em nhất thời")
        self.label2 = QLabel("         Diana Đẫm máu")
        self.label3 = QLabel("         Kiến Dàng")
        self.scanBtn = QPushButton("Scan user to Hack")
        self.connectBtn = QPushButton("Connect to user")

        parentLayout.addWidget(self.label1)
        parentLayout.addWidget(self.label2)
        parentLayout.addWidget(self.label3)
        parentLayout.addWidget(self.scanBtn)
        parentLayout.addWidget(self.connectBtn)

        centerWidget = QWidget()
        centerWidget.setLayout(parentLayout)
        self.setCentralWidget(centerWidget)
        