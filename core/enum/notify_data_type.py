from enum import Enum

class NotifyDataType(Enum):
    AFE = 0xA0
    IMU = 0xA1
    TEMP = 0xA2

    @staticmethod
    def get(value: int):
        # Iterate over the enum members and return the one matching the value
        for cmd in NotifyDataType:
            if cmd.value == value:
                return cmd
        return None