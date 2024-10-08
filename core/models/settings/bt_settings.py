from dataclasses import dataclass
from typing import Optional

from core.enum.power_level import PowerLevel


@dataclass
class BTSettings:
    adv_name: Optional[str] = None
    adv_interval: Optional[float] = None
    connection_interval_min: Optional[float] = None
    connection_interval_max: Optional[float] = None
    slave_latency: Optional[float] = None
    transmit_power_level: Optional[PowerLevel] = None
    supervision_timeout: Optional[float] = None
