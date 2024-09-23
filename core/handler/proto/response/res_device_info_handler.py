from core.models import DeviceInfo
from proto import old_brp_pb2 as brp


class ResDeviceInfoHandler:
    @staticmethod
    def parse(packet: brp.Packet) -> DeviceInfo:
        return DeviceInfo(
            serial_number=packet.response.dev_info.serial_number,
            manufacturing_date=packet.response.dev_info.manufacturing_date,
            lot=packet.response.dev_info.lot,
            model=packet.response.dev_info.model,
            pcba_version=packet.response.dev_info.pcba_version,
            bootloader_version=packet.response.dev_info.bootloader_version,
            application_version=packet.response.dev_info.application_version,
            build_date=packet.response.dev_info.build_date
        )
