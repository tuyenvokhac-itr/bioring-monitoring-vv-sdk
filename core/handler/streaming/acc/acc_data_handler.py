from core.models import AccelData
import struct

class AccDataHandler:
    @staticmethod
    def parse(data: bytearray, length: int) -> AccelData:
        num_samples = int(length / 2)
        imu_data = struct.unpack(f"<{num_samples}h", data)
        for i in range(0, num_samples, 3):
            raw_x = imu_data[i]
            raw_y = imu_data[i + 1]
            raw_z = imu_data[i + 2]
        
        return AccelData(raw_x, raw_y, raw_z)