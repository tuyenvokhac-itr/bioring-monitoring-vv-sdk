from typing import List

from core.models import DeviceInfo
from core.callbacks.response_callback import ResponseCallback
from core.utils.list_utils import ListUtils
from errors.common_error import CommonError
from errors.common_result import CommonResult
from proto import brp_pb2 as brp


class ResDeviceInfoHandler:
    @staticmethod
    def handle(packet: brp.Packet, response_callbacks: List[ResponseCallback]):
        resp_callback = ListUtils.get_response_callback(response_callbacks, packet.sid)
        if resp_callback is not None:
            ack = packet.ack
            if ack.result.is_success:
                device_info = DeviceInfo(
                    serial_number=packet.response.dev_info.serial_number,
                    manufacturing_date=packet.response.dev_info.manufacturing_date,
                    lot=packet.response.dev_info.lot,
                    model=packet.response.dev_info.model,
                    pcba_version=packet.response.dev_info.pcba_version,
                    bootloader_version=packet.response.dev_info.bootloader_version,
                    application_version=packet.response.dev_info.application_version,
                    build_date=packet.response.dev_info.build_date
                )
                resp_callback.callback(CommonResult(is_success=True), device_info)
            else:
                resp_callback.callback(CommonResult(
                    is_success=False,
                    error=CommonError(packet.response.cid, ack.error)
                ))
            response_callbacks.remove(resp_callback)
