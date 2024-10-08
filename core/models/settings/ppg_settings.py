from dataclasses import dataclass
from typing import Optional

from core.enum.ppg_sampling_rate import PpgSamplingRate


@dataclass
class PpgSettings:
    enable: Optional[bool] = None
    enable_red_led: Optional[bool] = None
    enable_ir_led: Optional[bool] = None
    red_led_current: Optional[float] = None
    ir_led_current: Optional[float] = None
    sampling_rate: Optional[PpgSamplingRate] = None
