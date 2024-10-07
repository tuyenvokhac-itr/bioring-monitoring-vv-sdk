from enum import Enum

import proto.brp_pb2 as brp


class AccelSamplingRate(Enum):
    ACC_SAMPLE_RATE_12Hz5 = 1
    ACC_SAMPLE_RATE_26Hz = 2
    ACC_SAMPLE_RATE_52Hz = 3

    def to_brp_accel_sample_rate(self) -> brp.AccelSampleRate:
        mapping = {
            AccelSamplingRate.ACC_SAMPLE_RATE_12Hz5: brp.AccelSampleRate.ACCEL_SAMPLE_RATE_12Hz5,
            AccelSamplingRate.ACC_SAMPLE_RATE_26Hz: brp.AccelSampleRate.ACCEL_SAMPLE_RATE_26Hz,
            AccelSamplingRate.ACC_SAMPLE_RATE_52Hz: brp.AccelSampleRate.ACCEL_SAMPLE_RATE_52Hz,
        }
        return mapping.get(self, None)
