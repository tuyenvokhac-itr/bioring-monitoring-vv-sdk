from enum import Enum

import proto.brp_pb2 as brp


class PowerLevel(Enum):
    NEG_20 = -20
    NEG_16 = -16
    NEG_12 = -12
    NEG_6 = -6
    POS_0 = 0
    POS_4 = 4

    def to_brp_power_level(self) -> brp.BleTxPowerLevel:
        mapping = {
            PowerLevel.NEG_20: brp.BleTxPowerLevel.BLE_TX_POWER_LEVEL_NEG_20,
            PowerLevel.NEG_16: brp.BleTxPowerLevel.BLE_TX_POWER_LEVEL_NEG_16,
            PowerLevel.NEG_12: brp.BleTxPowerLevel.BLE_TX_POWER_LEVEL_NEG_12,
            PowerLevel.NEG_6: brp.BleTxPowerLevel.BLE_TX_POWER_LEVEL_NEG_6,
            PowerLevel.POS_0: brp.BleTxPowerLevel.BLE_TX_POWER_LEVEL_POS_0,
            PowerLevel.POS_4: brp.BleTxPowerLevel.BLE_TX_POWER_LEVEL_POS_4,
        }
        return mapping.get(self, None)
