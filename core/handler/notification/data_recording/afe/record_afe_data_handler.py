from typing import List

from ble.bt_device import BTDevice
from core.utils.compute_helper import ComputeHelper
from errors.common_error import CommonError
from managers.record_data_callback import RecordDataCallback
from proto import brp_pb2 as brp


class RecordAfeDataHandler:
    @staticmethod
    def handle(device: BTDevice, packet: brp.Packet, record_data_callbacks: List[RecordDataCallback]):
        try:
            ecg_data, ppg_data = ComputeHelper.decode_afe_data(packet)
            for callback in record_data_callbacks:
                callback.on_ecg_recorded(device, ecg_data)
                callback.on_ppg_recorded(device, ppg_data)

        except  Exception as e:
            print(e)
            for callback in record_data_callbacks:
                callback.on_record_error(
                    device,
                    CommonError.ACC_RECORD_ERROR
                )
