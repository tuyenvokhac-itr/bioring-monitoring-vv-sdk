from proto import brp_pb2 as brp
from ble.ble_manager import BleManager
import time
from ble.ble_constant import BleConstant

class GetDeviceInfoCommand:
    @staticmethod
    def send(ble_manager: BleManager):
        pkt = brp.Packet()
        pkt.sid = int(time.time() * 1000)
        pkt.type = brp.PacketType.PACKET_TYPE_COMMAND
        pkt.command.cid = brp.CommandId.CID_DEV_INFO_GET
        
        pkt_value = pkt.SerializeToString()
        ble_manager.write(BleConstant.BRS_UUID_CHAR_TX, pkt_value)
        
        