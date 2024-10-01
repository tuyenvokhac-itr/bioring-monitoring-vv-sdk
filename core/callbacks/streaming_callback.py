from collections.abc import Callable
from dataclasses import dataclass

from core.enum.sensor_type import SensorType


@dataclass
class StreamingCallback:
    sid: int
    sensor_type: SensorType
    callback: Callable