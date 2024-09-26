from enum import Enum

import proto.brp_pb2 as brp


class AccelFullScaleRange(Enum):
    ACC_FS_2G = 0
    ACC_FS_16G = 1
    ACC_FS_4G = 2
    ACC_FS_8G = 3

    def to_brp_accel_full_scale_range(self) -> brp.AccelFullScale:
        mapping = {
            AccelFullScaleRange.ACC_FS_2G: brp.AccelFullScale.ACC_FULLSCALE_2g,
            AccelFullScaleRange.ACC_FS_16G: brp.AccelFullScale.ACC_FULLSCALE_16g,
            AccelFullScaleRange.ACC_FS_4G: brp.AccelFullScale.ACC_FULLSCALE_4g,
            AccelFullScaleRange.ACC_FS_8G: brp.AccelFullScale.ACC_FULLSCALE_8g,
        }
        return mapping.get(self, None)
