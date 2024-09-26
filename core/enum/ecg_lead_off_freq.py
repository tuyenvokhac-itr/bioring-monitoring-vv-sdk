from enum import Enum

import proto.brp_pb2 as brp


class EcgLeadOffFreq(Enum):
    ECG_LEAD_OFF_FREQ_DISABLE = 0
    ECG_LEAD_OFF_FREQ_8192HZ = 1
    ECG_LEAD_OFF_FREQ_4096HZ = 2
    ECG_LEAD_OFF_FREQ_2048HZ = 3
    ECG_LEAD_OFF_FREQ_1024HZ = 4
    ECG_LEAD_OFF_FREQ_512HZ = 5
    ECG_LEAD_OFF_FREQ_256HZ = 6
    ECG_LEAD_OFF_FREQ_128HZ = 7

    def to_brp_ecg_lead_off_freq(self) -> brp.EcgLeadOffFreq:
        mapping = {
            EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_DISABLE: brp.EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_DISABLE,
            EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_8192HZ: brp.EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_8192HZ,
            EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_4096HZ: brp.EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_4096HZ,
            EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_2048HZ: brp.EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_2048HZ,
            EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_1024HZ: brp.EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_1024HZ,
            EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_512HZ: brp.EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_512HZ,
            EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_256HZ: brp.EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_256HZ,
            EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_128HZ: brp.EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_128HZ,
        }
        return mapping.get(self, None)
