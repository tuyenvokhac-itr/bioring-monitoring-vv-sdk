from typing import List

from core.callbacks.response_callback import ResponseCallback
from core.models.raw_data.samples_threshold import SamplesThreshold
from core.utils.list_utils import ListUtils
from errors.common_error import CommonError
from errors.common_result import CommonResult
from proto import brp_pb2 as brp


class GetRecordSamplesHandler:
    @staticmethod
    def handle(packet: brp.Packet, response_callbacks: List[ResponseCallback]) -> None:
        resp_callback = ListUtils.get_response_callback(response_callbacks, packet.sid)
        if resp_callback is not None:
            if packet.response.result.is_success:
                samples = SamplesThreshold(
                    max_accel_samples = packet.response.sample_threshold.max_accel_samples,
                    max_ecg_samples=packet.response.sample_threshold.max_ecg_samples,
                    max_ppg_samples=packet.response.sample_threshold.max_ppg_samples,
                    max_temp_samples=packet.response.sample_threshold.max_temp_samples,
                )

                resp_callback.callback(CommonResult(is_success=True), samples)
            else:
                resp_callback.callback(CommonResult(
                    is_success=False,
                    error=CommonError(packet.response.cid, packet.response.result.error)
                ))
            response_callbacks.remove(resp_callback)
