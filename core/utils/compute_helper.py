import logging
from typing import List

from core.enum.fifo_data_type import FifoDataType
from core.models.raw_data.accel_data import AccelData
from core.models.raw_data.ecg_data import EcgData
from core.models.raw_data.ppg_data import PpgData
from core.models.raw_data.temp_data import TempData
from proto import brp_pb2 as brp


# def uint32_to_int16(value):
#     # Extract lower 16 bits
#     lower_16_bits = value & 0xFFFF
#     # Convert to signed 16-bit integer
#     signed_int16 = np.int16(lower_16_bits)
#     return signed_int16


class ComputeHelper:
    @staticmethod
    def convert_to_signed_int(number, bit) -> int:
        # Maximum positive value for a signed number
        max_value = (1 << (bit - 1)) - 1

        # Converting it to a decimal value
        decimal_value = number if number <= max_value else number - (1 << bit)
        return decimal_value

    @staticmethod
    def decode_acc_data(packet: brp.Packet) -> AccelData:
        start_time = packet.notification.raw_accel.start_time
        raw_accel = list(packet.notification.raw_accel)
        is_eot = False
        if packet.notification.raw_accel.HasField('eot'):
            is_eot = packet.notification.raw_accel.eot

        accel_data = AccelData(
            start_time=start_time,
            x=[], y=[], z=[],
            is_eot=is_eot
        )

        # Each AccData consists of 3 values (X, Y, Z)
        samples = int(len(raw_accel) / 3)

        for i in range(samples):
            idx = i * 3
            raw_x = raw_accel[idx]
            raw_y = raw_accel[idx + 1]
            raw_z = raw_accel[idx + 2]

            accel_data.x.append(raw_x)
            accel_data.y.append(raw_y)
            accel_data.z.append(raw_z)

        return accel_data

    @staticmethod
    def decode_temp_data(packet: brp.Packet) -> TempData:
        start_time = packet.notification.raw_temp.start_time
        raw_temp = list(packet.notification.raw_temp)
        is_eot = False
        if packet.notification.raw_temp.HasField('eot'):
            is_eot = packet.notification.raw_accel.eot

        temp_data = TempData(
            start_time=start_time,
            value=raw_temp,
            is_eot=is_eot
        )

        return temp_data

    @staticmethod
    def decode_afe_data(packet: brp.Packet) -> (EcgData, PpgData):
        start_time = packet.notification.raw_afe.start_time
        afe_raw = list(packet.notification.raw_afe.data)
        is_eot = False
        if packet.notification.raw_afe.HasField('eot'):
            is_eot = packet.notification.raw_afe.eot

        ppg_red_value: List[int] = []
        ppg_ir_value: List[int] = []
        ecg_value: List[int] = []

        for i in range(len(afe_raw)):
            fifo_type = (afe_raw[i] & 0x00f00000) >> 20

            match fifo_type:
                # PPG Red
                case FifoDataType.PPG_MEAS_1.value:
                    ppg_red_raw_sample = afe_raw[i] & 0x000fffff
                    ppg_red_signed_value = ComputeHelper.convert_to_signed_int(ppg_red_raw_sample, 20)
                    ppg_red_value.append(ppg_red_signed_value)

                # PPG IR
                case FifoDataType.PPG_MEAS_2.value:
                    ppg_ir_raw_sample = afe_raw[i] & 0x000fffff
                    ppg_ir_signed_value = ComputeHelper.convert_to_signed_int(ppg_ir_raw_sample, 20)
                    ppg_ir_value.append(ppg_ir_signed_value)

                # ECG
                case FifoDataType.ECG_AND_FAST_RECOVER_FLAG.value:
                    ecg_raw_sample = afe_raw[i] & 0x0003ffff
                    ecg_signed_value = ComputeHelper.convert_to_signed_int(ecg_raw_sample, 18)
                    ecg_value.append(ecg_signed_value)
                case _:
                    logging.error("Invalid FIFO type")

        ppg_data = PpgData(
            start_type=start_time,
            red=ppg_red_value,
            ir=ppg_ir_value,
            is_eot=is_eot
        )

        ecg_data = EcgData(
            start_time=start_time,
            data=ecg_value,
            is_eot=is_eot
        )

        return ecg_data, ppg_data
