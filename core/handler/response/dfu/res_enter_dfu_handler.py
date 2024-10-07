from typing import List

from core.callbacks.response_callback import ResponseCallback
from core.utils.list_utils import ListUtils
from errors.common_error import CommonError
from errors.common_result import CommonResult
from proto import brp_pb2 as brp


class ResEnterDfuHandler:
    @staticmethod
    def handle(packet: brp.Packet, response_callbacks: List[ResponseCallback]):
        resp_callback = ListUtils.get_response_callback(response_callbacks, packet.sid)
        if resp_callback is not None:
            if packet.response.result.is_success:
                resp_callback.callback()
            else:
                resp_callback.callback(result=CommonResult(
                    is_success=False,
                    error=CommonError(packet.response.cid, packet.response.result.error)
                ))
            response_callbacks.remove(resp_callback)
