from dataclasses import dataclass
from typing import List

@dataclass
class PpgData:
    start_type: int
    red: List[int]
    ir: List[int]