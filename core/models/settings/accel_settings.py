from dataclasses import dataclass
from typing import Optional

from core.enum.accel_full_scale_range import AccelFullScaleRange
from core.enum.accel_sampling_rate import AccelSamplingRate


@dataclass
class AccelSettings:
    enable: Optional[bool] = None
    sampling_rate: Optional[AccelSamplingRate] = None
    full_scale_range: Optional[AccelFullScaleRange] = None