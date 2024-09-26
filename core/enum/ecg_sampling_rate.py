from enum import Enum

import proto.brp_pb2 as brp


class EcgSamplingRate(Enum):
    ECG_SAMPLE_RATE_64HZ = 0
    ECG_SAMPLE_RATE_128HZ = 1
    ECG_SAMPLE_RATE_256HZ = 2

    def to_brp_ecg_sample_rate(self) -> brp.EcgSampleRate:
        mapping = {
            EcgSamplingRate.ECG_SAMPLE_RATE_64HZ: brp.EcgSampleRate.ECG_SAMPLE_RATE_64HZ,
            EcgSamplingRate.ECG_SAMPLE_RATE_128HZ: brp.EcgSampleRate.ECG_SAMPLE_RATE_128HZ,
            EcgSamplingRate.ECG_SAMPLE_RATE_256HZ: brp.EcgSampleRate.ECG_SAMPLE_RATE_256HZ,
        }
        return mapping.get(self, None)
