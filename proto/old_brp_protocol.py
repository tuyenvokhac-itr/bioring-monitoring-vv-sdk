import time
import proto.old_brp_pb2 as brp
import logging


class Protocol:
    PACKET_TYPE_AFE_DATA = 0xA0
    PACKET_TYPE_IMU_DATA = 0xA1
    PACKET_TYPE_TEMPERATURE_DATA = 0xA2
    PACKET_TYPE_LOG_DATA = 0xA3
    PACKET_TYPE_POWER_DATA = 0xA4
    PACKET_TYPE_SELF_TEST_DATA   = 0xA5

    def __init__(self, debug=False):
        self.debug = debug
        self.log = logging.getLogger(__name__)
        if self.debug:
            self.log.setLevel(logging.DEBUG)
        else:
            self.log.setLevel(logging.INFO)

    def encode_command(self, command_id: brp.CommandId):
        command = brp.Packet()
        command.sid = int(time.time() * 1000)
        command.type = brp.PacketType.PACKET_TYPE_COMMAND
        command.command.cid = command_id
        logging.debug(f"Encode Command:\n{str(command)}")
        return command.SerializeToString()

    def encode_ack(self, noti_packet: brp.Packet, ack_result: brp.AckResponseCode):
        ack = brp.Packet()
        ack.sid = noti_packet.sid
        ack.type = brp.PacketType.PACKET_TYPE_ACK
        ack.ack.nid = noti_packet.notification.nid
        ack.ack.result = ack_result
        logging.debug(f"Encode ACK:\n{str(ack)}")
        return ack.SerializeToString()

    def decode_streaming_data(self, data: bytearray):
        type = data[0]
        sequence_number = int.from_bytes(data[1:3], "little", signed=False)
        length = int.from_bytes(data[3:5], "little", signed=False)
        value = data[5:length+5]
        return (type, sequence_number, length, value)
