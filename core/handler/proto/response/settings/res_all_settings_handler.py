from typing import List

from core.command_callback import ResponseCallback
from core.models.settings.accel_settings import AccelSettings
from core.models.settings.bt_settings import BTSettings
from core.models.settings.device_settings import DeviceSettings
from core.models.settings.ecg_settings import EcgSettings, LeadOffSettings
from core.models.settings.log_settings import LogSettings
from core.models.settings.ppg_settings import PpgSettings
from core.utils.list_utils import ListUtils
from errors.common_error import CommonError
from errors.common_result import CommonResult
from proto import brp_pb2 as brp


class ResAllSettingsHandler:
    @staticmethod
    def handle(packet: brp.Packet, response_callbacks: List[ResponseCallback]) -> None:
        resp_callback = ListUtils.get_response_callback(response_callbacks, packet.sid)
        if resp_callback is not None:
            ack = packet.ack
            if ack.result.is_success:
                lead_off_settings = LeadOffSettings(
                    enable=packet.response.all_dev_settings.lead_off_enable,
                    mode=packet.response.all_dev_settings.lead_off_params.lead_off_mode,
                    current_polarity=packet.response.all_dev_settings.lead_off_params.lead_off_current_polarity,
                    current_magnitude=packet.response.all_dev_settings.lead_off_params.lead_off_current_magnitude,
                    voltage_threshold=packet.response.all_dev_settings.lead_off_params.lead_off_voltage_threshold,
                    lead_off_frequency=packet.response.all_dev_settings.lead_off_params.lead_off_freq,
                )

                ecg_settings = EcgSettings(
                    enable=packet.response.all_dev_settings.ecg_settings.ecg_enable,
                    sampling_rate=packet.response.all_dev_settings.ecg_settings.sample_rate,
                    pga_gain=packet.response.all_dev_settings.ecg_settings.ecg_gain.pga_gain,
                    ina_gain=packet.response.all_dev_settings.ecg_settings.ecg_gain.ina_gain,
                    ina_range=packet.response.all_dev_settings.ecg_settings.ecg_gain.ina_range,
                    input_polarity=packet.response.all_dev_settings.ecg_settings.input_polarity,
                    lead_off_settings=lead_off_settings
                )

                ppg_settings = PpgSettings(
                    enable=packet.response.all_dev_settings.ppg_settings.ppg_enable,
                    sampling_rate=packet.response.all_dev_settings.ppg_settings.sample_rate,
                    enable_red_led=packet.response.all_dev_settings.ppg_settings.ppg_led_settings.red_led_enable,
                    enable_ir_led=packet.response.all_dev_settings.ppg_settings.ppg_led_settings.ir_led_enable,
                    red_led_current=packet.response.all_dev_settings.ppg_settings.ppg_led_settings.red_led_current,
                    ir_led_current=packet.response.all_dev_settings.ppg_settings.ppg_led_settings.ir_led_current,
                )

                accel_settings = AccelSettings(
                    enable=packet.response.all_dev_settings.accel_settings.accel_enable,
                    sampling_rate=packet.response.all_dev_settings.accel_settings.sample_rate,
                    full_scale_range=packet.response.all_dev_settings.accel_settings.accel_full_scale,
                )

                bluetooth_settings = BTSettings(
                    adv_name=packet.response.all_dev_settings.ble_settings.advertising_name,
                    adv_interval=packet.response.all_dev_settings.ble_settings.advertising_interval,
                    connection_interval_min=packet.response.all_dev_settings.ble_settings.connect_params.connect_intv_min,
                    connection_interval_max=packet.response.all_dev_settings.ble_settings.connect_params.connect_intv_max,
                    slave_latency=packet.response.all_dev_settings.ble_settings.connect_params.slave_latency,
                    supervision_timeout=packet.response.all_dev_settings.ble_settings.connect_params.conn_sup_timeout,
                    transmit_power_level=packet.response.all_dev_settings.ble_settings.tx_power_level,
                )

                log_settings = LogSettings(
                    enable=packet.response.all_dev_settings.log_settings.log_enable,
                    levels=packet.response.all_dev_settings.log_settings.log_level,
                )

                settings = DeviceSettings(
                    ecg_settings=ecg_settings,
                    ppg_settings=ppg_settings,
                    accel_settings=accel_settings,
                    bluetooth_settings=bluetooth_settings,
                    log_settings=log_settings
                )

                resp_callback.callback(CommonResult(is_success=True), settings)
            else:
                resp_callback.callback(CommonResult(
                    is_success=False,
                    error=CommonError(packet.response.cid, ack.error)
                ))
            response_callbacks.remove(resp_callback)
