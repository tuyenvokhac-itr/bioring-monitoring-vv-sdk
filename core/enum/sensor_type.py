from enum import Enum

import proto.brp_pb2 as brp


class SensorType(Enum):
    ACCEL = 1
    ECG = 2
    PPG = 4
    TEMP = 8

    def to_brp_sensor_type(self) -> brp.SensorType:
        mapping = {
            SensorType.ACCEL: brp.SensorType.SENSOR_TYPE_ACCEL,
            SensorType.ECG: brp.SensorType.SENSOR_TYPE_ECG,
            SensorType.PPG: brp.SensorType.SENSOR_TYPE_PPG,
            SensorType.TEMP: brp.SensorType.SENSOR_TYPE_TEMP,
        }
        return mapping.get(self, None)
