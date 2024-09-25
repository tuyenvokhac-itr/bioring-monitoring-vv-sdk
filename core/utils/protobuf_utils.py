import proto.brp_pb2 as brp
from core.enum.general_enum import SensorType


class ProtobufUtils:
    @staticmethod
    def to_brp_sensor_type(sensor_type: SensorType) -> brp.SensorType:
        match sensor_type:
            case SensorType.PPG:
                return brp.SensorType.SENSOR_TYPE_PPG
            case SensorType.ECG:
                return brp.SensorType.SENSOR_TYPE_ECG
            case SensorType.ACCEL:
                return brp.SensorType.SENSOR_TYPE_ACCEL
            case SensorType.TEMP:
                return brp.SensorType.SENSOR_TYPE_TEMP
            case _:
                return None
