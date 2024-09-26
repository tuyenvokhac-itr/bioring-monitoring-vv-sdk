from enum import Enum

import proto.brp_pb2 as brp


class EcgLeadOffCurrentMagnitude(Enum):
    ECG_LEAD_OFF_IMAG_0 = 0
    ECG_LEAD_OFF_IMAG_5 = 1
    ECG_LEAD_OFF_IMAG_10 = 2
    ECG_LEAD_OFF_IMAG_20 = 3
    ECG_LEAD_OFF_IMAG_50 = 4
    ECG_LEAD_OFF_IMAG_100 = 5
    ECG_LEAD_OFF_IMAG_200 = 6
    ECG_LEAD_OFF_IMAG_400 = 7

    def to_brp_ecg_lead_off_current_magnitude(self) -> brp.EcgLeadOffCurrentMagnitude:
        mapping = {
            EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_0: brp.EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_0,
            EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_5: brp.EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_5,
            EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_10: brp.EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_10,
            EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_20: brp.EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_20,
            EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_50: brp.EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_50,
            EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_100: brp.EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_100,
            EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_200: brp.EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_200,
            EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_400: brp.EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_400,
        }
        return mapping.get(self, None)
