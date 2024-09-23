from PyQt6.QtCore import QObject, pyqtSignal

class BluetoothStateReceiver(QObject):
    bluetoothStateChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
