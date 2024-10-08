from typing import Any, Callable, Awaitable

from bleak import BleakClient

from ble.ble_constant import BleConstant
from core.models.settings.accel_settings import AccelSettings
from proto import brp_pb2 as brp


class SetAccelSettingsCommand:
    @staticmethod
    async def send(
            sid: int,
            client: BleakClient,
            accel_settings: AccelSettings,
            write_char: Callable[[BleakClient, str, Any], Awaitable[None]]
    ):
        pkt = brp.Packet()
        pkt.sid = sid
        pkt.type = brp.PacketType.PACKET_TYPE_COMMAND
        pkt.command.cid = brp.CommandId.CID_ACCEL_SETTINGS_SET
        if accel_settings.enable is not None:
            pkt.command.all_dev_settings.accel_settings.accel_enable = accel_settings.enable

        if accel_settings.sampling_rate is not None:
            pkt.command.all_dev_settings.accel_settings.sample_rate = accel_settings.sampling_rate.to_brp_accel_sample_rate()

        if accel_settings.full_scale_range is not None:
            pkt.command.all_dev_settings.accel_settings.accel_full_scale = accel_settings.full_scale_range.to_brp_accel_full_scale_range()

        pkt_value = pkt.SerializeToString()
        await write_char(client, BleConstant.BRS_UUID_CHAR_TX, pkt_value)
