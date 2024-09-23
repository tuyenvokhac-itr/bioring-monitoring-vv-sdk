from dataclasses import dataclass
from typing import Optional

from core.enum.sensor_settings_enums import AccelSamplingRate, AccelFullScaleRange


@dataclass
class AccelSettings:
    enable: Optional[bool]
    sampling_rate: Optional[AccelSamplingRate]
    full_scale_range: Optional[AccelFullScaleRange]