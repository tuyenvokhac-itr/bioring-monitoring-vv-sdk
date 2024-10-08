from dataclasses import dataclass
from typing import List, Optional

from core.enum.log_level import LogLevel


@dataclass
class LogSettings:
    enable: Optional[bool] = None
    levels: Optional[List[LogLevel]] = None
