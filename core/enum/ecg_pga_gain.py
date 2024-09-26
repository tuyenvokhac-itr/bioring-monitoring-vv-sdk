from enum import Enum

import proto.brp_pb2 as brp


class EcgPgaGain(Enum):
    PGA_GAIN_1 = 0
    PGA_GAIN_2 = 1
    PGA_GAIN_4 = 2
    PGA_GAIN_8 = 3
    PGA_GAIN_16 = 7

    def to_brp_ecg_pga_gain(self) -> brp.EcgPgaGain:
        mapping = {
            EcgPgaGain.PGA_GAIN_1: brp.EcgPgaGain.ECG_PGA_GAIN_1,
            EcgPgaGain.PGA_GAIN_2: brp.EcgPgaGain.ECG_PGA_GAIN_2,
            EcgPgaGain.PGA_GAIN_4: brp.EcgPgaGain.ECG_PGA_GAIN_4,
            EcgPgaGain.PGA_GAIN_8: brp.EcgPgaGain.ECG_PGA_GAIN_8,
            EcgPgaGain.PGA_GAIN_16: brp.EcgPgaGain.ECG_PGA_GAIN_16,
        }
        return mapping.get(self, None)
