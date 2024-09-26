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
    enable: Optional[bool]
    mode: Optional[EcgLeadOffMode]
    current_polarity: Optional[EcgLeadOffCurrentPolarity]
    current_magnitude: Optional[EcgLeadOffCurrentMagnitude]
    voltage_threshold: Optional[EcgLeadOffVoltageThreshold]
    lead_off_frequency: Optional[EcgLeadOffFreq]


@dataclass
class EcgSettings:
    enable: Optional[bool]
    sampling_rate: Optional[EcgSamplingRate]
    pga_gain: Optional[EcgPgaGain]
    ina_gain: Optional[EcgInaGain]
    ina_range: Optional[EcgInaRange]
    input_polarity: Optional[EcgInputPolarity]
    lead_off_settings: Optional[LeadOffSettings]
