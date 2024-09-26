from enum import Enum

import proto.brp_pb2 as brp


class EcgInaRange(Enum):
    ECG_INA_GAIN_RGE_0 = 0
    ECG_INA_GAIN_RGE_1 = 1
    ECG_INA_GAIN_RGE_2 = 2
    ECG_INA_GAIN_RGE_3 = 3

    def to_brp_ecg_ina_range(self) -> brp.EcgInaRange:
        mapping = {
            EcgInaRange.ECG_INA_GAIN_RGE_0: brp.EcgInaRange.ECG_INA_GAIN_RGE_0,
            EcgInaRange.ECG_INA_GAIN_RGE_1: brp.EcgInaRange.ECG_INA_GAIN_RGE_1,
            EcgInaRange.ECG_INA_GAIN_RGE_2: brp.EcgInaRange.ECG_INA_GAIN_RGE_2,
            EcgInaRange.ECG_INA_GAIN_RGE_3: brp.EcgInaRange.ECG_INA_GAIN_RGE_3,
        }
        return mapping.get(self, None)
