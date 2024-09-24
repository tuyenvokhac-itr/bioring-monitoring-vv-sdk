from collections.abc import Callable
from dataclasses import dataclass

@dataclass
class ResponseCallback:
    sid: int
    callback: Callable