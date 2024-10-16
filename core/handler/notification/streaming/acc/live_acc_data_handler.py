from collections.abc import Callable
from typing import List

from core.enum.sensor_type import SensorType
from core.callbacks.streaming_callback import StreamingCallback
from core.utils.compute_helper import ComputeHelper
from core.utils.list_utils import ListUtils
from errors.common_error import CommonError
from errors.common_result import CommonResult
from proto import brp_pb2 as brp


class LiveAccDataHandler:
    @staticmethod
    def handle(
            packet: brp.Packet,
            streaming_callbacks: List[StreamingCallback],
            prev_sequence_number: int,
            on_sequence_number_updated: Callable[[int], None]
    ):
        acc_streaming_callbacks = ListUtils.get_streaming_callbacks(streaming_callbacks, SensorType.ACCEL)

        try:
            sequence_number = packet.notification.raw_accel.sequence_number
            accel_data = ComputeHelper.decode_acc_data(packet)
            packet_lost = 0 if prev_sequence_number == 0 else sequence_number - prev_sequence_number
            on_sequence_number_updated(sequence_number)

            for callback in acc_streaming_callbacks:
                callback.callback(CommonResult(True), accel_data, packet_lost)

        except Exception as e:
            for callback in acc_streaming_callbacks:
                callback.callback(
                    CommonResult(is_success=False, error=CommonError.ACC_STREAMING_ERROR),
                    None, 0
                )