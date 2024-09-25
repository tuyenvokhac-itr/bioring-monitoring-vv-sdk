from typing import List

from core.command_callback import ResponseCallback
from core.models.protocol import Protocol
from core.utils.list_utils import ListUtils
from errors.common_error import CommonError
from errors.common_result import CommonResult
from proto import brp_pb2 as brp


class ResProtocolInfoHandler:
    @staticmethod
    def handle(packet: brp.Packet, response_callbacks: List[ResponseCallback]) -> None:
        resp_callback = ListUtils.get_response_callback(response_callbacks, packet.sid)
        if resp_callback is not None:
            ack = packet.ack
            if ack.result.is_success:
                protocol = Protocol(
                    version=packet.response.protocol_info.version,
                )

                resp_callback.callback(CommonResult(is_success=True), protocol)
            else:
                resp_callback.callback(CommonResult(
                    is_success=False,
                    error=CommonError(packet.response.cid, ack.error)
                ))
            response_callbacks.remove(resp_callback)
