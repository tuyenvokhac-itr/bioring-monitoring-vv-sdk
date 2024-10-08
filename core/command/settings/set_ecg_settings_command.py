from typing import Any, Callable, Awaitable

from bleak import BleakClient

from ble.ble_constant import BleConstant
from core.models.settings.ecg_settings import EcgSettings
from proto import brp_pb2 as brp


class SetEcgSettingsCommand:
    @staticmethod
    async def send(
            sid: int,
            client: BleakClient,
            ecg_settings: EcgSettings,
            write_char: Callable[[BleakClient, str, Any], Awaitable[None]]
    ):
        pkt = brp.Packet()
        pkt.sid = sid
        pkt.type = brp.PacketType.PACKET_TYPE_COMMAND
        pkt.command.cid = brp.CommandId.CID_ECG_SETTINGS_SET

        if ecg_settings.enable is not None:
            pkt.command.all_dev_settings.ecg_settings.ecg_enable = ecg_settings.enable

        if ecg_settings.sampling_rate is not None:
            pkt.command.all_dev_settings.ecg_settings.sample_rate = ecg_settings.sampling_rate.to_brp_ecg_sample_rate()

        if ecg_settings.pga_gain is not None:
            pkt.command.all_dev_settings.ecg_settings.ecg_gain.pga_gain = ecg_settings.pga_gain.to_brp_ecg_pga_gain()

        if ecg_settings.ina_gain is not None:
            pkt.command.all_dev_settings.ecg_settings.ecg_gain.ina_gain = ecg_settings.ina_gain.to_brp_ecg_ina_gain()

        if ecg_settings.ina_range is not None:
            pkt.command.all_dev_settings.ecg_settings.ecg_gain.ina_range = ecg_settings.ina_range.to_brp_ecg_ina_range()

        if ecg_settings.input_polarity is not None:
            pkt.command.all_dev_settings.ecg_settings.input_polarity = ecg_settings.input_polarity.to_brp_ecg_input_polarity()

        if ecg_settings.lead_off_enable is not None:
            pkt.command.all_dev_settings.ecg_settings.lead_off_enable = ecg_settings.lead_off_enable

        if ecg_settings.lead_off_settings is not None:
            if ecg_settings.lead_off_settings.mode is not None:
                pkt.command.all_dev_settings.ecg_settings.lead_off_params.lead_off_mode = ecg_settings.lead_off_settings.mode.to_brp_ecg_lead_off_mode()

            if ecg_settings.lead_off_settings.current_polarity is not None:
                pkt.command.all_dev_settings.ecg_settings.lead_off_params.lead_off_current_polarity = ecg_settings.lead_off_settings.current_polarity.to_brp_ecg_lead_off_current_polarity()

            if ecg_settings.lead_off_settings.current_magnitude is not None:
                pkt.command.all_dev_settings.ecg_settings.lead_off_params.lead_off_current_magnitude = ecg_settings.lead_off_settings.current_magnitude.to_brp_ecg_lead_off_current_magnitude()

            if ecg_settings.lead_off_settings.voltage_threshold is not None:
                pkt.command.all_dev_settings.ecg_settings.lead_off_params.lead_off_voltage_threshold = ecg_settings.lead_off_settings.voltage_threshold.to_brp_ecg_lead_off_voltage_threshold()

            if ecg_settings.lead_off_settings.lead_off_frequency is not None:
                pkt.command.all_dev_settings.ecg_settings.lead_off_params.lead_off_freq = ecg_settings.lead_off_settings.lead_off_frequency.to_brp_ecg_lead_off_freq()

        pkt_value = pkt.SerializeToString()
        await write_char(client, BleConstant.BRS_UUID_CHAR_TX, pkt_value)
