from enum import Enum

import proto.brp_pb2 as brp


class PpgSamplingRate(Enum):
    ECG_SAMPLE_RATE_64HZ = 0
    ECG_SAMPLE_RATE_128HZ = 1
    ECG_SAMPLE_RATE_256HZ = 2

    def to_brp_ppg_sample_rate(self) -> brp.PpgSampleRate:
        mapping = {
            PpgSamplingRate.ECG_SAMPLE_RATE_64HZ: brp.PpgSampleRate.PPG_SAMPLE_RATE_64HZ,
            PpgSamplingRate.ECG_SAMPLE_RATE_128HZ: brp.PpgSampleRate.PPG_SAMPLE_RATE_128HZ,
            PpgSamplingRate.ECG_SAMPLE_RATE_256HZ: brp.PpgSampleRate.PPG_SAMPLE_RATE_256HZ,
        }
        return mapping.get(self, None)
