from typing import Any, Callable
from proto import old_brp_pb2 as brp
from ble.old_ble_manager import OldBleManager
import time
from ble.ble_constant import BleConstant


class LiveAccDataCommand:
    @staticmethod
    def send(isStart: bool, write_chars: Callable[[str, Any], None]):
        pkt = brp.Packet()
        pkt.sid = int(time.time() * 1000)
        pkt.type = brp.PacketType.PACKET_TYPE_COMMAND
        if isStart:
            pkt.command.cid = brp.CommandId.CID_STREAMING_DATA_START
        else:
            pkt.command.cid = brp.CommandId.CID_STREAMING_DATA_STOP
        pkt.command.sensor_type = brp.SensorType.SENSOR_TYPE_IMU

        pkt_value = pkt.SerializeToString()
        write_chars(BleConstant.BRS_UUID_CHAR_TX, pkt_value)
