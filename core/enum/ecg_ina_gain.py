from enum import Enum

import proto.brp_pb2 as brp


class EcgInaGain(Enum):
    INA_GAIN_0 = 0
    INA_GAIN_1 = 1
    INA_GAIN_2 = 2
    INA_GAIN_3 = 3

    def to_brp_ecg_ina_gain(self) -> brp.EcgInaGain:
        mapping = {
            EcgInaGain.INA_GAIN_0: brp.EcgInaGain.ECG_INA_GAIN_0,
            EcgInaGain.INA_GAIN_1: brp.EcgInaGain.ECG_INA_GAIN_1,
            EcgInaGain.INA_GAIN_2: brp.EcgInaGain.ECG_INA_GAIN_2,
            EcgInaGain.INA_GAIN_3: brp.EcgInaGain.ECG_INA_GAIN_3,
        }
        return mapping.get(self, None)
