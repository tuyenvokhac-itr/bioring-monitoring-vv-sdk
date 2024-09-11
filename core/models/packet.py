from dataclasses import dataclass
from core.enum.notify_data_type import NotifyDataType

@dataclass
class Packet:
    type: NotifyDataType
    data: bytearray