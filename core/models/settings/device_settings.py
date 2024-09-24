from dataclasses import dataclass

from core.models.settings.bt_settings import BTSettings
from core.models.settings.accel_settings import AccelSettings
from core.models.settings.ecg_settings import EcgSettings
from core.models.settings.log_settings import LogSettings
from core.models.settings.ppg_settings import PpgSettings


@dataclass
class DeviceSettings:
    ecg_settings: EcgSettings
    ppg_settings: PpgSettings
    accel_settings: AccelSettings
    bluetooth_settings: BTSettings
    log_settings: LogSettings