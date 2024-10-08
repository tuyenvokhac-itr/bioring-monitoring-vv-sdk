from enum import Enum

import proto.brp_pb2 as brp


class PpgSamplingRate(Enum):
    PPG_SAMPLE_RATE_64HZ = 0
    PPG_SAMPLE_RATE_128HZ = 1
    PPG_SAMPLE_RATE_256HZ = 2

    def to_brp_ppg_sample_rate(self) -> brp.PpgSampleRate:
        mapping = {
            PpgSamplingRate.PPG_SAMPLE_RATE_64HZ: brp.PpgSampleRate.PPG_SAMPLE_RATE_64HZ,
            PpgSamplingRate.PPG_SAMPLE_RATE_128HZ: brp.PpgSampleRate.PPG_SAMPLE_RATE_128HZ,
            PpgSamplingRate.PPG_SAMPLE_RATE_256HZ: brp.PpgSampleRate.PPG_SAMPLE_RATE_256HZ,
        }
        return mapping.get(self, None)
