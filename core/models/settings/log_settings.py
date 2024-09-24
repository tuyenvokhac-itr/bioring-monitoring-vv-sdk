from dataclasses import dataclass

from core.enum.settings_enums import LogLevel
from typing import List


@dataclass
class LogSettings:
    enable: bool
    levels: List[LogLevel]
