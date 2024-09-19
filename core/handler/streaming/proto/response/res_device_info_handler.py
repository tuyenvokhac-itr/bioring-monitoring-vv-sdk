from core.models import DeviceInfo
from proto import brp_pb2 as brp


class ResDeviceInfoHandler:
    @staticmethod
    def parse(packet: brp.Packet) -> DeviceInfo:
        return DeviceInfo(
            hw_version=packet.response.dev_info.hardware_version,
            fw_version=packet.response.dev_info.firmware_version,
            serial_number=packet.response.dev_info.serial_number,
            model=packet.response.dev_info.model,
        )
