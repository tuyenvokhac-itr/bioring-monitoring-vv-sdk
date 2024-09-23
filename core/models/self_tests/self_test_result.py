from dataclasses import dataclass


@dataclass
class SelfTestResult:
    afe: bool
    accel: bool
    temp: bool
    wireless_charger: bool
    fuel_gauge: bool
