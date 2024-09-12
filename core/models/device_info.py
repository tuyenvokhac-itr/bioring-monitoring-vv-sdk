from dataclasses import dataclass


@dataclass
class DeviceInfo:
    hw_version: str
    fw_version: str
    serial_number: str
    model: str
