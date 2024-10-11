from typing import List

from ble.bt_device import BTDevice
from core.utils.protobuf_utils import ProtobufUtils
from errors.common_error import CommonError
from managers.record_data_callback import RecordDataCallback
from proto import brp_pb2 as brp


class RecordDataFinishedHandler:
    @staticmethod
    def handle(device: BTDevice, packet: brp.Packet, record_data_callbacks: List[RecordDataCallback]):
        try:
            pkt_sensor_type = packet.notification.sensor_type
            sensor_type = ProtobufUtils.to_sensor_type(pkt_sensor_type)
            for callback in record_data_callbacks:
                callback.on_record_finished(device, sensor_type)

        except  Exception as e:
            pass
            for callback in record_data_callbacks:
                callback.on_record_error(
                    device,
                    CommonError.ACC_RECORD_ERROR
                )
