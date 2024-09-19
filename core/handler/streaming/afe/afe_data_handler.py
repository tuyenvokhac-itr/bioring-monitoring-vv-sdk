from typing import List
from core.enum.fifo_data_type import FifoDataType
from core.models import AccData
import struct
import logging

# from core.utils import compute_utils


# PPG and ECG
class AfeDataHandler:
    @staticmethod
    def handle(data: bytearray) -> AccData:
        return AfeDataHandler._parse(data)
    
    @staticmethod
    def parse(data: bytearray, length: int) -> AccData:
        ecg_data = List[int]
        ppg_red_data = List[int]
        ppg_ir_data = List[int] 
        
        num_samples = int(length / 4)
        afe_data = struct.unpack(f"<{num_samples}I", data)
        logging.debug(f"afe_data: {afe_data}")

        for i in range(0, num_samples, 1):
            fifo_type = afe_data[i] >> 20

            # if fifo_type == FifoDataType.ECG_AND_FAST_RECOVER_FLAG.value:
            #     ecg_data_one_sample = afe_data[i] & 0x0003FFFF  # Remove the Flag
            #     ecg_data_one_sample = compute_utils.create_a_signed_number(ecg_data_one_sample, 18)

            #     # Write to file ECG ADC value
            #     self.write_record_file(RecordType.ECG, [ecg_data_one_sample])

            #     # Calculate mV value for only display
            #     if self.ecg_mv_unit is True:
            #         # V_ECG(mV) = ADC_VALUE * V_REF_ADC / (2^17 * ECG_GAIN)
            #         ecg_data_one_sample = (ecg_data_one_sample * 1000) / (pow(2, 17) * self.ecg_gain_val)

            #     # logging.debug("ECG data:", ecg_data_one_sample)
            #     ecg_data.append(ecg_data_one_sample)
            #     ecg_idx_data.append(len(ecg_data))
            # else:
            #     ppg_data = afe_data[i] & 0x000FFFFF  # Remove the Flag

            #     ppg_data = compute_utils.create_a_signed_number(ppg_data, 20)

            #     if fifo_type == FifoDataType.PPG_MEAS_1.value:
            #         red_data.append(ppg_data)
            #         red_idx_data.append(len(red_data))
            #         # logging.debug("AFE measure 1, RED:", ppg_data)
            #         self.ppg_red_data = ppg_data
            #         self.ppg_red_flag = True
            #     elif fifo_type == FifoDataType.PPG_MEAS_2.value:
            #         ir_data.append(ppg_data)
            #         ir_idx_data.append(len(ir_data))
            #         # logging.debug("AFE measure 2, IR:", ppg_data)
            #         self.ppg_ir_data = ppg_data
            #         self.ppg_ir_flag = True
            #     elif fifo_type == FifoDataType.PPG_EXP_OVF.value:
            #         logging.warning("PPG_EXP_OVF_DATA")
            #     else:
            #         # logging.error("AFE format error:", afe_data[i])
            #         return -1

            #     if (self.ppg_red_flag is True) and (self.ppg_ir_flag is True):
            #         self.write_record_file(RecordType.PPG, [self.ppg_red_data, self.ppg_ir_data])
            #         self.ppg_red_flag = False
            #         self.ppg_ir_flag = False