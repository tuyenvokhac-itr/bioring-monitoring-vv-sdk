from typing import Any, Callable, Awaitable

from bleak import BleakClient

from ble.ble_constant import BleConstant
from core.models.settings.ecg_settings import EcgSettings
from proto import brp_pb2 as brp


class SettingsCommand:
    @staticmethod
    async def get_all_settings(
            sid: int, client: BleakClient,
            write_char: Callable[[BleakClient, str, Any], Awaitable[None]]
    ):
        pkt = brp.Packet()
        pkt.sid = sid
        pkt.type = brp.PacketType.PACKET_TYPE_COMMAND
        pkt.command.cid = brp.CommandId.CID_ALL_SETTINGS_GET

        pkt_value = pkt.SerializeToString()
        await write_char(client, BleConstant.BRS_UUID_CHAR_TX, pkt_value)

    @staticmethod
    async def set_ecg_settings(
            sid: int, client: BleakClient, ecg_settings: EcgSettings,
            write_char: Callable[[BleakClient, str, Any], Awaitable[None]]
    ):
        pkt = brp.Packet()
        pkt.sid = sid
        pkt.type = brp.PacketType.PACKET_TYPE_COMMAND
        pkt.command.cid = brp.CommandId.CID_ECG_SETTINGS_SET

        pkt.command.all_dev_settings.ecg_settings.ecg_enable = ecg_settings.enable
        pkt.command.all_dev_settings.ecg_settings.sample_rate = ecg_settings.sampling_rate
        pkt.command.all_dev_settings.ecg_settings.ecg_gain.pga_gain = ecg_settings.pga_gain
        pkt.command.all_dev_settings.ecg_settings.ecg_gain.ina_gain = ecg_settings.ina_gain
        pkt.command.all_dev_settings.ecg_settings.ecg_gain.ina_range = ecg_settings.ina_range
        pkt.command.all_dev_settings.ecg_settings.input_polarity = ecg_settings.input_polarity
        pkt.command.all_dev_settings.ecg_settings.lead_off_enable = ecg_settings.lead_off_settings.enable
        pkt.command.all_dev_settings.ecg_settings.lead_off_params.lead_off_mode = ecg_settings.lead_off_settings.mode
        pkt.command.all_dev_settings.ecg_settings.lead_off_params.lead_off_current_polarity = ecg_settings.lead_off_settings.current_polarity
        pkt.command.all_dev_settings.ecg_settings.lead_off_params.lead_off_current_magnitude = ecg_settings.lead_off_settings.current_magnitude
        pkt.command.all_dev_settings.ecg_settings.lead_off_params.lead_off_voltage_threshold = ecg_settings.lead_off_settings.voltage_threshold
        pkt.command.all_dev_settings.ecg_settings.lead_off_params.lead_off_freq = ecg_settings.lead_off_settings.lead_off_frequency

        pkt_value = pkt.SerializeToString()
        await write_char(client, BleConstant.BRS_UUID_CHAR_TX, pkt_value)
