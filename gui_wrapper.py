from PyQt6 import QtWidgets

from qt_gui.ring_gui import Ui_RingGui


class GuiWrapper(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = Ui_RingGui()
        self.uic.setupUi(self)
        self.setWindowTitle("Test Bioring SDK")