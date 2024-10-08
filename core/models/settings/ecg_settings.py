from dataclasses import dataclass
from typing import Optional

from core.enum.ecg_ina_gain import EcgInaGain
from core.enum.ecg_ina_range import EcgInaRange
from core.enum.ecg_input_polarity import EcgInputPolarity
from core.enum.ecg_lead_off_current_magnitude import EcgLeadOffCurrentMagnitude
from core.enum.ecg_lead_off_current_polarity import EcgLeadOffCurrentPolarity
from core.enum.ecg_lead_off_freq import EcgLeadOffFreq
from core.enum.ecg_lead_off_mode import EcgLeadOffMode
from core.enum.ecg_lead_off_voltage_threshold import EcgLeadOffVoltageThreshold
from core.enum.ecg_pga_gain import EcgPgaGain
from core.enum.ecg_sampling_rate import EcgSamplingRate


@dataclass
class LeadOffSettings:
    mode: Optional[EcgLeadOffMode] = None
    current_polarity: Optional[EcgLeadOffCurrentPolarity] = None
    current_magnitude: Optional[EcgLeadOffCurrentMagnitude] = None
    voltage_threshold: Optional[EcgLeadOffVoltageThreshold] = None
    lead_off_frequency: Optional[EcgLeadOffFreq] = None


@dataclass
class EcgSettings:
    enable: Optional[bool] = None
    sampling_rate: Optional[EcgSamplingRate] = None
    pga_gain: Optional[EcgPgaGain] = None
    ina_gain: Optional[EcgInaGain] = None
    ina_range: Optional[EcgInaRange] = None
    input_polarity: Optional[EcgInputPolarity] = None
    lead_off_settings: Optional[LeadOffSettings] = None
    lead_off_enable: Optional[bool] = None
