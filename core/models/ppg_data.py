from dataclasses import dataclass
from typing import List

@dataclass
class PpgData:
    red: List[int]
    ir: List[int]