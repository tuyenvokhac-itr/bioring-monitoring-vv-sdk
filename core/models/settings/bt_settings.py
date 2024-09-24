from dataclasses import dataclass
from typing import Optional

from core.enum.settings_enums import PowerLevel


@dataclass
class BTSettings:
    adv_name: Optional[str]
    adv_interval: Optional[float]
    connection_interval_min: Optional[float]
    connection_interval_max: Optional[float]
    slave_latency: Optional[float]
    supervision_timeout: Optional[float]
    transmit_power_level: Optional[PowerLevel]
