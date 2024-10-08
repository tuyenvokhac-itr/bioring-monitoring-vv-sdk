from dataclasses import dataclass
from typing import Optional

from core.models.settings.bt_settings import BTSettings
from core.models.settings.accel_settings import AccelSettings
from core.models.settings.ecg_settings import EcgSettings
from core.models.settings.log_settings import LogSettings
from core.models.settings.ppg_settings import PpgSettings


@dataclass
class DeviceSettings:
    ecg_settings: Optional[EcgSettings] = None
    ppg_settings: Optional[PpgSettings] = None
    accel_settings: Optional[AccelSettings] = None
    bluetooth_settings: Optional[BTSettings] = None
    log_settings: Optional[LogSettings] = None