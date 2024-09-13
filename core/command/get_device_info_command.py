from proto import brp_pb2 as brp
from ble.ble_manager import BleManager
import time
from ble.ble_constant import BleConstant
from typing import Any, Callable


class GetDeviceInfoCommand:
    @staticmethod
    def send(write_chars: Callable[[str, Any], None]):
        pkt = brp.Packet()
        pkt.sid = int(time.time() * 1000)
        pkt.type = brp.PacketType.PACKET_TYPE_COMMAND
        pkt.command.cid = brp.CommandId.CID_DEV_INFO_GET

        pkt_value = pkt.SerializeToString()
        write_chars(BleConstant.BRS_UUID_CHAR_TX, pkt_value)
