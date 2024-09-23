from enum import Enum

class NotifyDataType(Enum):
    AFE = 0xA0
    ACC = 0xA1
    TEMP = 0xA2
    LOG = 0xA3
    POWER = 0xA4
    SELF_TEST = 0xA5

    @staticmethod
    def get(value: int):
        # Iterate over the enum members and return the one matching the value
        for cmd in NotifyDataType:
            if cmd.value == value:
                return cmd
        return None