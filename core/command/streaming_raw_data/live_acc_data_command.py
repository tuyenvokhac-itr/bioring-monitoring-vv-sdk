from typing import Any, Callable, Awaitable

from bleak import BleakClient

from ble.ble_constant import BleConstant
from proto import brp_pb2 as brp


class LiveAccDataCommand:
    @staticmethod
    async def send(
            sid: int, client: BleakClient, is_start: bool,
            write_char: Callable[[BleakClient, str, Any], Awaitable[None]]
    ):
        pkt = brp.Packet()
        pkt.sid = sid
        pkt.type = brp.PacketType.PACKET_TYPE_COMMAND
        if is_start:
            pkt.command.cid = brp.CommandId.CID_STREAMING_DATA_START
        else:
            pkt.command.cid = brp.CommandId.CID_STREAMING_DATA_STOP
        pkt.command.sensor_type = brp.SensorType.SENSOR_TYPE_ACCEL

        pkt_value = pkt.SerializeToString()
        await write_char(client, BleConstant.BRS_UUID_CHAR_TX, pkt_value)
