from ble.bt_device import BTDevice
from core.core_handler import CoreHandler
from core.utils.compute_helper import ComputeHelper
from errors.common_error import CommonError
from proto import brp_pb2 as brp


class RecordAfeDataHandler:
    @staticmethod
    def handle(device: BTDevice, packet: brp.Packet):
        try:
            ecg_data, ppg_data = ComputeHelper.decode_afe_data(packet)
            for callback in CoreHandler().record_data_callbacks:
                callback.on_ecg_recorded(device, ecg_data)
                callback.on_ppg_recorded(device, ppg_data)

        except  Exception as e:
            for callback in CoreHandler().record_data_callbacks:
                callback.on_record_error(
                    device,
                    CommonError.ACC_RECORD_ERROR
                )
