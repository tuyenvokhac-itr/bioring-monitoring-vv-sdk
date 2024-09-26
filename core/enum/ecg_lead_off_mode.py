from enum import Enum

import proto.brp_pb2 as brp


class EcgLeadOffMode(Enum):
    ECG_LEAD_OFF_DC = 0
    ECG_LEAD_OFF_AC = 1

    def to_brp_ecg_lead_off_mode(self) -> brp.EcgLeadOffMode:
        mapping = {
            EcgLeadOffMode.ECG_LEAD_OFF_DC: brp.EcgLeadOffMode.ECG_LEAD_OFF_DC,
            EcgLeadOffMode.ECG_LEAD_OFF_AC: brp.EcgLeadOffMode.ECG_LEAD_OFF_AC,
        }
        return mapping.get(self, None)
