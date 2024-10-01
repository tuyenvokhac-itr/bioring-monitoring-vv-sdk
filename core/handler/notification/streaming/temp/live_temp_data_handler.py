from typing import List, Callable

from core.enum.sensor_type import SensorType
from core.callbacks.streaming_callback import StreamingCallback
from core.utils.compute_helper import ComputeHelper
from errors.common_error import CommonError
from errors.common_result import CommonResult
from proto import brp_pb2 as brp


class LiveTempDataHandler:
    @staticmethod
    def handle(
            packet: brp.Packet,
            streaming_callbacks: List[StreamingCallback],
            prev_sequence_number: int,
            on_sequence_number_updated: Callable[[int], None]
    ):
        temp_streaming_callbacks = [
            callback for callback in streaming_callbacks if
            callback.sensor_type == SensorType.TEMP
        ]

        try:
            sequence_number = packet.notification.sequence_number
            temp_data = ComputeHelper.decode_temp_data(packet)
            packet_lost = 0 if prev_sequence_number == 0 else sequence_number - prev_sequence_number
            on_sequence_number_updated(sequence_number)

            for callback in temp_streaming_callbacks:
                callback.callback(CommonResult(True), temp_data, packet_lost)

        except Exception as e:
            for callback in temp_streaming_callbacks:
                callback.callback(
                    CommonResult(is_success=False, error=CommonError.TEMP_STREAMING_ERROR),
                    None, 0
                )
            print(f'Error in LiveTempDataHandler: {e}')
