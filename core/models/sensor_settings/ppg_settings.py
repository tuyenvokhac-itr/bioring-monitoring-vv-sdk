from dataclasses import dataclass
from typing import Optional

from core.enum.sensor_settings_enums import PpgSamplingRate


@dataclass
class PpgSettings:
    enable: Optional[bool]
    enable_red_led: Optional[bool]
    enable_ir_led: Optional[bool]
    red_led_current: Optional[float]
    ir_led_current: Optional[float]
    sampling_rate: Optional[PpgSamplingRate]