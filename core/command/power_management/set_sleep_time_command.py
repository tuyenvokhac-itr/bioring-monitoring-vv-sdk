from typing import Any, Callable, Awaitable

from bleak import BleakClient

from ble.ble_constant import BleConstant
from proto import brp_pb2 as brp


class SetSleepTimeCommand:
    @staticmethod
    async def send(
            sid: int,
            client: BleakClient,
            seconds: int,
            write_char: Callable[[BleakClient, str, Any], Awaitable[None]]
    ):
        pkt = brp.Packet()
        pkt.sid = sid
        pkt.type = brp.PacketType.PACKET_TYPE_COMMAND
        pkt.command.cid = brp.CommandId.CID_DEV_PRE_SLEEP_TIMEOUT_SET

        pkt.command.pre_sleep_timeout = seconds

        pkt_value = pkt.SerializeToString()
        await write_char(client, BleConstant.BRS_UUID_CHAR_TX, pkt_value)
