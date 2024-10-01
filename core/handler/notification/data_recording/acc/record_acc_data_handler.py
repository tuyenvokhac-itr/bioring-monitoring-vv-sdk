from ble.bt_device import BTDevice
from core.core_handler import CoreHandler
from core.utils.compute_helper import ComputeHelper
from errors.common_error import CommonError
from proto import brp_pb2 as brp


class RecordAccDataHandler:
    @staticmethod
    def handle(device: BTDevice, packet: brp.Packet):
        try:
            accel_data = ComputeHelper.decode_acc_data(packet)
            for callback in CoreHandler().record_data_callbacks:
                callback.on_accel_recorded(device, accel_data)

        except  Exception as e:
            for callback in CoreHandler().record_data_callbacks:
                callback.on_record_error(
                    device,
                    CommonError.ACC_RECORD_ERROR
                )