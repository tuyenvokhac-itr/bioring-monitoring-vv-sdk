from dataclasses import dataclass
from typing import List


@dataclass
class EcgData:
    start_time: int
    data: List[int]
    is_eot: bool = False
