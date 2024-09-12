from proto import brp_pb2 as brp
from ble.ble_manager import BleManager
import time
from ble.ble_constant import BleConstant


class LivePpgDataCommand:
    @staticmethod
    def send(isStart: bool, ble_manager: BleManager):
        pkt = brp.Packet()
        pkt.sid = int(time.time() * 1000)
        pkt.command.sensor_type = brp.SensorType.SENSOR_TYPE_PPG
        if isStart:
            pkt.command.cid = brp.CommandId.CID_STREAMING_DATA_START
        else:
            pkt.command.cid = brp.CommandId.CID_STREAMING_DATA_STOP
        pkt.type = brp.PacketType.PACKET_TYPE_COMMAND

        pkt_value = pkt.SerializeToString()
        ble_manager.write(BleConstant.BRS_UUID_CHAR_TX, pkt_value)
