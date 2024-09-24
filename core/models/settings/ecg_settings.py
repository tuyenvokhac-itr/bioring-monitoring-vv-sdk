from dataclasses import dataclass
from typing import Optional

from core.enum.settings_enums import EcgSamplingRate, EcgPgaGain, EcgInaGain, EcgInaRange, EcgInputPolarity, \
    EcgLeadOffMode, EcgLeadOffCurrentMagnitude, EcgLeadOffVoltageThreshold, EcgLeadOffFreq


@dataclass
class LeadOffSettings:
    enable: Optional[bool]
    mode: Optional[EcgLeadOffMode]
    current_polarity: Optional[EcgInputPolarity]
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
