from enum import Enum

class SensorType(Enum):
    ACCEL = 1
    ECG = 2
    PPG = 4
    TEMP = 8

class AppType(Enum):
    BOOT_LOADER = 0
    APPLICATION = 1

class ChargingError(Enum):
    OK = 0
    IC_TEMP = 1
    PROTOCOL = 2
    BATT_CONNECT = 4
    BATT_TEMP = 8
    TCM_TIMEOUT = 12
    CCM_TIMEOUT = 16
    CVM_TIMEOUT = 20

class ChargingStatus(Enum):
    DISCHARGING = 0
    CHARGING = 1