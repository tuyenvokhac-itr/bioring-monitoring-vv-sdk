from dataclasses import dataclass


@dataclass
class DeviceInfo:
    serial_number: str
    manufacturing_date: str
    lot: str
    model: str
    pcba_version: str
    bootloader_version: str
    application_version: str
    build_date: str
