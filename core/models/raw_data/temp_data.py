from dataclasses import dataclass
from typing import List


@dataclass
class TempData:
    start_time: int
    value: List[float]
    is_eot: bool = False
