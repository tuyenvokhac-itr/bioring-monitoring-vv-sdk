from enum import Enum

import proto.brp_pb2 as brp


class EcgLeadOffCurrentPolarity(Enum):
    ECG_LEAD_OFF_NON_INVERTED = 0
    ECG_LEAD_OFF_INVERTED = 1

    def to_brp_ecg_lead_off_current_polarity(self) -> brp.EcgLeadOffCurrentPolarity:
        mapping = {
            EcgLeadOffCurrentPolarity.ECG_LEAD_OFF_NON_INVERTED: brp.EcgLeadOffCurrentPolarity.ECG_LEAD_OFF_NON_INVERTED,
            EcgLeadOffCurrentPolarity.ECG_LEAD_OFF_INVERTED: brp.EcgLeadOffCurrentPolarity.ECG_LEAD_OFF_INVERTED,
        }
        return mapping.get(self, None)
