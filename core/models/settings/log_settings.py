from dataclasses import dataclass

from typing import List

from core.enum.log_level import LogLevel


@dataclass
class   LogSettings:
    enable: bool
    levels: List[LogLevel]
