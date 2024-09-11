from dataclasses import dataclass
from typing import List

@dataclass
class EcgData:
    data: List[int]