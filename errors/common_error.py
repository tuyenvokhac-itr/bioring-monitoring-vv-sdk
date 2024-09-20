from enum import Enum

class CommonError(Enum):
    CONNECTION_FAILED = (101, "Failed to connect to device.")
    DEVICE_DISCONNECTED = (102, "Device disconnected.")

    def __init__(self, code, message):
        self._code = code
        self._message = message

    @property
    def code(self):
        """Returns the error code."""
        return self._code

    @property
    def message(self):
        """Returns the error message."""
        return self._message

    def __str__(self):
        return f"{self.code}: {self.message}"