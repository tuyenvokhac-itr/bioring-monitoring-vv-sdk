from typing import List

from ble.bt_device import BTDevice
from core.utils.compute_helper import ComputeHelper
from errors.common_error import CommonError
from managers.record_data_callback import RecordDataCallback
from proto import brp_pb2 as brp


class RecordAccDataHandler:
    @staticmethod
    def handle(device: BTDevice, packet: brp.Packet, record_data_callbacks: List[RecordDataCallback]):
        try:
            accel_data = ComputeHelper.decode_acc_data(packet)
            for callback in record_data_callbacks:
                callback.on_accel_recorded(device, accel_data)

        except  Exception as e:
            for callback in record_data_callbacks:
                callback.on_record_error(
                    device,
                    CommonError.ACC_RECORD_ERROR
                )
