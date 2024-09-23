from dataclasses import dataclass

@dataclass
class SamplesThreshold:
    max_accel_samples: int
    max_ecg_samples: int
    max_ppg_samples: int
    max_temp_samples: int