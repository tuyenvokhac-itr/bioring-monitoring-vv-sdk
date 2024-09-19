from core.models import TempData
import struct


class TempDataHandler:
    @staticmethod
    def parse(data: bytearray) -> TempData:
        num_samples = 1
        temp_data = struct.unpack(f"<{num_samples}f", data)
        return temp_data[0]
