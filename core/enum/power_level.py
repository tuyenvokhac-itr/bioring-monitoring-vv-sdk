from enum import Enum

import proto.brp_pb2 as brp


class PowerLevel(Enum):
    POS_0 = 0
    POS_4 = 4

    def to_brp_power_level(self) -> brp.BleTxPowerLevel:
        mapping = {
            PowerLevel.POS_0: brp.BleTxPowerLevel.BLE_TX_POWER_LEVEL_0,
            PowerLevel.POS_4: brp.BleTxPowerLevel.BLE_TX_POWER_LEVEL_4,
        }
        return mapping.get(self, None)
