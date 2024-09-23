from dataclasses import dataclass
from typing import List

@dataclass
class TempData:
    start_type: int
    value: List[float]