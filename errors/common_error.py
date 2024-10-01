from enum import Enum


class CommonError(Enum):
    CONNECTION_FAILED = (101, "Failed to connect to device.")
    DEVICE_DISCONNECTED = (102, "Device disconnected.")

    # Streaming
    ACC_STREAMING_ERROR = (301, "ACC streaming error")
    ECG_STREAMING_ERROR = (302, "ECG streaming error")
    PPG_STREAMING_ERROR = (303, "PPG streaming error")
    TEMP_STREAMING_ERROR = (304, "TEMP streaming error")

    # Record
    ACC_RECORD_ERROR = (401, "ACC record error")
    AFE_RECORD_ERROR = (402, "ECG record error")
    TEMP_RECORD_ERROR = (403, "TEMP record error")

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
