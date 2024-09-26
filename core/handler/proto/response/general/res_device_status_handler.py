from typing import List

from core.command_callback import ResponseCallback
from core.models.device_status import DeviceStatus
from core.models.self_tests.self_test_result import SelfTestResult
from core.utils.list_utils import ListUtils
from core.utils.protobuf_utils import ProtobufUtils
from errors.common_error import CommonError
from errors.common_result import CommonResult
from proto import brp_pb2 as brp


class ResDeviceStatusHandler:
    @staticmethod
    def handle(packet: brp.Packet, response_callbacks: List[ResponseCallback]) -> None:
        resp_callback = ListUtils.get_response_callback(response_callbacks, packet.sid)
        if resp_callback is not None:
            ack = packet.ack
            if ack.result.is_success:
                bist_result = SelfTestResult(
                    afe=packet.response.dev_status.bist_result.afe,
                    accel=packet.response.dev_status.bist_result.accel,
                    temp=packet.response.dev_status.bist_result.temperature,
                    wireless_charger=packet.response.dev_status.bist_result.wireless_charger,
                    fuel_gauge=packet.response.dev_status.bist_result.fuel_gauge
                )

                post_result = SelfTestResult(
                    afe=packet.response.dev_status.post_result.afe,
                    accel=packet.response.dev_status.post_result.accel,
                    temp=packet.response.dev_status.post_result.temperature,
                    wireless_charger=packet.response.dev_status.post_result.wireless_charger,
                    fuel_gauge=packet.response.dev_status.post_result.fuel_gauge
                )

                device_status = DeviceStatus(
                    current_app=ProtobufUtils.to_app_type(packet.response.dev_status.current_app),
                    device_time=packet.response.dev_status.device_time,
                    bist_result=bist_result,
                    bist_timestamp=packet.response.dev_status.bist_timestamp,
                    post_result=post_result,
                    post_timestamp=packet.response.dev_status.post_timestamp,
                    is_charging=ProtobufUtils.to_charging_status(packet.response.dev_status.charging_status),
                    charging_error=ProtobufUtils.to_charging_error(packet.response.dev_status.charging_error),
                    battery_level=packet.response.dev_status.battery_level,
                )

                resp_callback.callback(CommonResult(is_success=True), device_status)
            else:
                resp_callback.callback(CommonResult(
                    is_success=False,
                    error=CommonError(packet.response.cid, ack.error)
                ))
            response_callbacks.remove(resp_callback)
