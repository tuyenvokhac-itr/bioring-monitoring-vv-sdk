from typing import Any, Callable, Awaitable

from bleak import BleakClient

from ble.ble_constant import BleConstant
from core.models.settings.ppg_settings import PpgSettings
from proto import brp_pb2 as brp


class SetPpgSettingsCommand:
    @staticmethod
    async def send(
            sid: int, client: BleakClient, ppg_settings: PpgSettings,
            write_char: Callable[[BleakClient, str, Any], Awaitable[None]]
    ):
        pkt = brp.Packet()
        pkt.sid = sid
        pkt.type = brp.PacketType.PACKET_TYPE_COMMAND
        pkt.command.cid = brp.CommandId.CID_PPG_SETTINGS_SET

        pkt.command.all_dev_settings.ppg_settings.ppg_enable = ppg_settings.enable
        pkt.command.all_dev_settings.ppg_settings.sample_rate = ppg_settings.sampling_rate.to_brp_ppg_sample_rate()
        pkt.command.all_dev_settings.ppg_settings.ppg_led_settings.red_led_enable = ppg_settings.enable_red_led
        pkt.command.all_dev_settings.ppg_settings.ppg_led_settings.ir_led_enable = ppg_settings.enable_ir_led
        pkt.command.all_dev_settings.ppg_settings.ppg_led_settings.red_led_current = ppg_settings.red_led_current
        pkt.command.all_dev_settings.ppg_settings.ppg_led_settings.ir_led_current = ppg_settings.ir_led_current

        pkt_value = pkt.SerializeToString()
        await write_char(client, BleConstant.BRS_UUID_CHAR_TX, pkt_value)
