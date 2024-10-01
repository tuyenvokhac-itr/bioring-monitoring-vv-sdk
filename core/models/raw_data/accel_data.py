from dataclasses import dataclass
from typing import List


@dataclass
class AccelData:
    start_time: int
    x: List[int]
    y: List[int]
    z: List[int]
    is_eot: bool = False
