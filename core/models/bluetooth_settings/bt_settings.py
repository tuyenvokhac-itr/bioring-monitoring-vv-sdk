from dataclasses import dataclass
from typing import Optional

from core.enum.bt_settings_enums import PowerLevel


@dataclass
class BTSettings:
    adv_name: Optional[str]
    adv_interval: Optional[int]
    connection_interval: Optional[int]
    slave_latency: Optional[int]
    supervision_timeout: Optional[int]
    transmit_power_level: Optional[PowerLevel]
