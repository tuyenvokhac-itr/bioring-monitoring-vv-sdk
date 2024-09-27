from typing import Any, Callable, Awaitable

from bleak import BleakClient

from ble.ble_constant import BleConstant
from core.models.settings.log_settings import LogSettings
from proto import brp_pb2 as brp


class SetLogSettingsCommand:
    @staticmethod
    async def send(
            sid: int, client: BleakClient, log_settings: LogSettings,
            write_char: Callable[[BleakClient, str, Any], Awaitable[None]]
    ):
        pkt = brp.Packet()
        pkt.sid = sid
        pkt.type = brp.PacketType.PACKET_TYPE_COMMAND
        pkt.command.cid = brp.CommandId.CID_LOG_SETTINGS_SET

        pkt.command.all_dev_settings.log_settings.log_enable = log_settings.enable
        pkt.command.all_dev_settings.log_settings[:] = list(map(lambda x: x.to_brp_log_level(), log_settings.levels))

        pkt_value = pkt.SerializeToString()
        await write_char(client, BleConstant.BRS_UUID_CHAR_TX, pkt_value)
