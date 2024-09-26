from typing import Any, Callable, Awaitable

from bleak import BleakClient

from ble.ble_constant import BleConstant
from core.utils.protobuf_utils import ProtobufUtils
from proto import brp_pb2 as brp


class StopStreamingDataCommand:
    @staticmethod
    async def send(
            sid: int, client: BleakClient, sensor_type: brp.SensorType,
            write_char: Callable[[BleakClient, str, Any], Awaitable[None]]
    ):
        pkt = brp.Packet()
        pkt.sid = sid
        pkt.type = brp.PacketType.PACKET_TYPE_COMMAND
        pkt.command.cid = brp.CommandId.CID_STREAMING_DATA_STOP
        pkt.command.sensor_type = ProtobufUtils.to_brp_sensor_type(sensor_type)

        pkt_value = pkt.SerializeToString()
        await write_char(client, BleConstant.BRS_UUID_CHAR_TX, pkt_value)
