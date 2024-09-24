from dataclasses import dataclass

from core.enum.general_enum import AppType, ChargingStatus, ChargingError
from core.models.self_tests.self_test_result import SelfTestResult


@dataclass
class DeviceStatus:
    current_app: AppType
    device_time: int
    post_result: SelfTestResult
    bist_result: SelfTestResult
    post_timestamp: int
    bist_timestamp: int
    is_charging: ChargingStatus
    battery_level: int
    charging_error: ChargingError