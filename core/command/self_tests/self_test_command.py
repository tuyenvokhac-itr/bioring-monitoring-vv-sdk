from typing import Any, Callable, Awaitable

from bleak import BleakClient

from ble.ble_constant import BleConstant
from proto import brp_pb2 as brp


class SetBistIntervalCommand:
    @staticmethod
    async def send(
            sid: int,
            client: BleakClient,
            interval: int,
            write_char: Callable[[BleakClient, str, Any], Awaitable[None]]
    ):
        pkt = brp.Packet()
        pkt.sid = sid
        pkt.type = brp.PacketType.PACKET_TYPE_COMMAND
        pkt.command.cid = brp.CommandId.CID_SELF_TEST_BIST_SET_INTERVAL
        pkt.command.bist_interval = interval

        pkt_value = pkt.SerializeToString()
        await write_char(client, BleConstant.BRS_UUID_CHAR_TX, pkt_value)
