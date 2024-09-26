from enum import Enum

import proto.brp_pb2 as brp


class EcgInputPolarity(Enum):
    ECG_INPUT_NON_INVERTED = 0
    ECG_INPUT_INVERTED = 1

    def to_brp_ecg_input_polarity(self) -> brp.EcgInputPolarity:
        mapping = {
            EcgInputPolarity.ECG_INPUT_NON_INVERTED: brp.EcgInputPolarity.ECG_INPUT_NON_INVERTED,
            EcgInputPolarity.ECG_INPUT_INVERTED: brp.EcgInputPolarity.ECG_INPUT_INVERTED,
        }
        return mapping.get(self, None)
