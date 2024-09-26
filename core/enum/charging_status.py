from enum import Enum

import proto.brp_pb2 as brp


class ChargingStatus(Enum):
    DISCHARGING = 0
    CHARGING = 1

    def to_brp_charging_status(self) -> brp.ChargingStatus:
        mapping = {
            ChargingStatus.DISCHARGING: brp.ChargingStatus.CHARGING_STATUS_DISCHARGING,
            ChargingStatus.CHARGING: brp.ChargingStatus.CHARGING_STATUS_CHARGING,
        }
        return mapping.get(self, None)
