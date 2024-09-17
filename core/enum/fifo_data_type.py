from enum import Enum


class FifoDataType(Enum):
    PPG_MEAS_1 = 0
    PPG_MEAS_2 = 1
    PPG_MEAS_3 = 2
    PPG_MEAS_4 = 3
    PPG_MEAS_5 = 4
    PPG_MEAS_6 = 5
    PPG_DARK = 6
    PPG_ALC_OVF = 7
    PPG_EXP_OVF = 8
    BIOZ_I = 9
    BIOZ_Q = 10
    ECG_AND_FAST_RECOVER_FLAG = 11