import logging
from typing import List, Callable

from core.enum.sensor_type import SensorType
from core.callbacks.streaming_callback import StreamingCallback
from core.utils.compute_helper import ComputeHelper
from core.utils.list_utils import ListUtils
from errors.common_error import CommonError
from errors.common_result import CommonResult
from proto import brp_pb2 as brp


class LiveAfeDataHandler:
    @staticmethod
    def handle(
            packet: brp.Packet,
            streaming_callbacks: List[StreamingCallback],
            prev_sequence_number: int,
            on_sequence_number_updated: Callable[[int], None]
    ):

        ppg_streaming_callbacks = ListUtils.get_streaming_callbacks(streaming_callbacks, SensorType.PPG)
        ecg_streaming_callbacks = ListUtils.get_streaming_callbacks(streaming_callbacks, SensorType.ECG)

        try:
            sequence_number = packet.notification.raw_afe.sequence_number
            ecg_data, ppg_data = ComputeHelper.decode_afe_data(packet)
            packet_lost = 0 if prev_sequence_number == 0 else sequence_number - prev_sequence_number
            on_sequence_number_updated(sequence_number)

            for callback in ppg_streaming_callbacks:
                callback.callback(CommonResult(True), ppg_data, packet_lost)

            for callback in ecg_streaming_callbacks:
                callback.callback(CommonResult(True), ecg_data, packet_lost)

        except Exception as e:
            for callback in ppg_streaming_callbacks:
                callback.callback(
                    CommonResult(is_success=False, error=CommonError.PPG_STREAMING_ERROR),
                    None, 0
                )
            for callback in ecg_streaming_callbacks:
                callback.callback(
                    CommonResult(is_success=False, error=CommonError.ECG_STREAMING_ERROR),
                    None, 0
                )
            print(f'Error in LiveAfeDataHandler: {e}')
            logging.error(f'Error in LiveAfeDataHandler: {e}')
