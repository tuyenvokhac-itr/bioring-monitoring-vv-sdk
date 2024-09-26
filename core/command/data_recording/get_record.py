from typing import Any, Callable, Awaitable

from bleak import BleakClient

from ble.ble_constant import BleConstant
from core.enum.sensor_type import SensorType
from proto import brp_pb2 as brp


class GetRecordCommand:
    @staticmethod
    async def send(
            sid: int, client: BleakClient, start_index: int,
            sensor_type: SensorType,
            write_char: Callable[[BleakClient, str, Any], Awaitable[None]]
    ):
        pkt = brp.Packet()
        pkt.sid = sid
        pkt.type = brp.PacketType.PACKET_TYPE_COMMAND
        pkt.command.cid = brp.CommandId.CID_RECORD_DATA_GET
        pkt.command.sensor_type = sensor_type.to_brp_sensor_type()
        # TODO: Add start_index to the packet
        pkt.command.start_index = start_index

        pkt_value = pkt.SerializeToString()
        await write_char(client, BleConstant.BRS_UUID_CHAR_TX, pkt_value)
