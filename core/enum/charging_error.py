from enum import Enum

import proto.brp_pb2 as brp


class ChargingError(Enum):
    OK = 0
    IC_TEMP = 1
    PROTOCOL = 2
    BATT_CONNECT = 4
    BATT_TEMP = 8
    TCM_TIMEOUT = 12
    CCM_TIMEOUT = 16
    CVM_TIMEOUT = 20

    def to_brp_charging_error(self) -> brp.ChargingError:
        mapping = {
            ChargingError.OK: brp.ChargingError.CHARGING_ERROR_OK,
            ChargingError.IC_TEMP: brp.ChargingError.CHARGING_ERROR_IC_TEMP,
            ChargingError.PROTOCOL: brp.ChargingError.CHARGING_ERROR_PROTOCOL,
            ChargingError.BATT_CONNECT: brp.ChargingError.CHARGING_ERROR_BATT_CONNECT,
            ChargingError.BATT_TEMP: brp.ChargingError.CHARGING_ERROR_BATT_TEMP,
            ChargingError.TCM_TIMEOUT: brp.ChargingError.CHARGING_ERROR_TCM_TIMEOUT,
            ChargingError.CCM_TIMEOUT: brp.ChargingError.CHARGING_ERROR_CCM_TIMEOUT,
            ChargingError.CVM_TIMEOUT: brp.ChargingError.CHARGING_ERROR_CVM_TIMEOUT,
        }
        return mapping.get(self, None)
