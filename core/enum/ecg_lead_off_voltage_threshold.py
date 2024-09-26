from enum import Enum

import proto.brp_pb2 as brp


class EcgLeadOffVoltageThreshold(Enum):
    ECG_LEAD_OFF_VOL_THRESH_25MV = 0
    ECG_LEAD_OFF_VOL_THRESH_50MV = 1
    ECG_LEAD_OFF_VOL_THRESH_75MV = 2
    ECG_LEAD_OFF_VOL_THRESH_100MV = 3
    ECG_LEAD_OFF_VOL_THRESH_125MV = 4
    ECG_LEAD_OFF_VOL_THRESH_150MV = 5
    ECG_LEAD_OFF_VOL_THRESH_175MV = 6
    ECG_LEAD_OFF_VOL_THRESH_200MV = 7
    ECG_LEAD_OFF_VOL_THRESH_225MV = 8
    ECG_LEAD_OFF_VOL_THRESH_250MV = 9
    ECG_LEAD_OFF_VOL_THRESH_275MV = 10
    ECG_LEAD_OFF_VOL_THRESH_300MV = 11
    ECG_LEAD_OFF_VOL_THRESH_325MV = 12
    ECG_LEAD_OFF_VOL_THRESH_350MV = 13
    ECG_LEAD_OFF_VOL_THRESH_375MV = 14
    ECG_LEAD_OFF_VOL_THRESH_400MV = 15

    def to_brp_ecg_lead_off_voltage_threshold(self) -> brp.EcgLeadOffVoltageThreshold:
        mapping = {
            EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_25MV: brp.EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_25MV,
            EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_50MV: brp.EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_50MV,
            EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_75MV: brp.EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_75MV,
            EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_100MV: brp.EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_100MV,
            EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_125MV: brp.EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_125MV,
            EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_150MV: brp.EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_150MV,
            EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_175MV: brp.EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_175MV,
            EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_200MV: brp.EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_200MV,
            EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_225MV: brp.EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_225MV,
            EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_250MV: brp.EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_250MV,
            EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_275MV: brp.EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_275MV,
            EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_300MV: brp.EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_300MV,
            EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_325MV: brp.EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_325MV,
            EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_350MV: brp.EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_350MV,
            EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_375MV: brp.EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_375MV,
            EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_400MV: brp.EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_400MV,
        }
        return mapping.get(self, None)
