from typing import List

from core.models.self_tests.self_test_result import SelfTestResult
from core.callbacks.response_callback import ResponseCallback
from core.utils.list_utils import ListUtils
from errors.common_error import CommonError
from errors.common_result import CommonResult
from proto import brp_pb2 as brp


class ResPostHandler:
    @staticmethod
    def handle(packet: brp.Packet, response_callbacks: List[ResponseCallback]):
        resp_callback = ListUtils.get_response_callback(response_callbacks, packet.sid)
        if resp_callback is not None:
            if packet.response.result.is_success:
                self_test_result = SelfTestResult(
                    afe=packet.response.self_test_data.afe,
                    accel=packet.response.self_test_data.accel,
                    temp=packet.response.self_test_data.temperature,
                    wireless_charger=packet.response.self_test_data.wireless_charger,
                    fuel_gauge=packet.response.self_test_data.fuel_gauge
                )
                resp_callback.callback(CommonResult(is_success=True), self_test_result)
            else:
                resp_callback.callback(CommonResult(
                    is_success=False,
                    error=CommonError(packet.response.cid, packet.response.result.error)
                ))
            response_callbacks.remove(resp_callback)
