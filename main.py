from ble.ble_manager import BleManager
from core.models import EcgData, PpgData
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from typing import List, Tuple, Callable
from bleak import BleakClient
from bioring_tool import BioRingTool


from PyQt6.QtWidgets import QApplication
from qt_gui import QTGuideWindow

def main():
    tool = BioRingTool()

    
if(__name__ == "__main__"):
    main()

