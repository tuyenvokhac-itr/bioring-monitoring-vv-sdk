from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QPalette, QColor

class Toast(QWidget):
    def __init__(self, message, duration=3000, parent=None):
        super().__init__(parent)
        self.duration = duration  # Duration in milliseconds

        # Set window flags to make it frameless and always on top
        self.setWindowFlags(
            Qt.WindowType.ToolTip |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        # Set up the label
        self.label = QLabel(message, self)
        self.label.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 180);
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont("Arial", 10))

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Adjust size based on content
        self.adjustSize()

        # Position the toast at the bottom-right corner of the parent
        if parent:
            parent_geometry = parent.geometry()
            x = parent_geometry.x() + parent_geometry.width() - self.width() - 20
            y = parent_geometry.y() + parent_geometry.height() - self.height() - 50
        else:
            screen_geometry = QApplication.primaryScreen().availableGeometry()
            x = screen_geometry.width() - self.width() - 20
            y = screen_geometry.height() - self.height() - 50
        self.move(x, y)

        # Initialize opacity for fade-in
        self.setWindowOpacity(0.0)
        self.show()

        # Fade-in animation
        self.fade_in = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in.setDuration(500)  # 0.5 seconds
        self.fade_in.setStartValue(0.0)
        self.fade_in.setEndValue(1.0)
        self.fade_in.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade_in.start()

        # Timer to start fade-out after duration
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.fade_out_animation)
        self.timer.setSingleShot(True)
        self.timer.start(self.duration)

    def fade_out_animation(self):
        # Fade-out animation
        self.fade_out = QPropertyAnimation(self, b"windowOpacity")
        self.fade_out.setDuration(500)  # 0.5 seconds
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.0)
        self.fade_out.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade_out.finished.connect(self.close)
        self.fade_out.start()
