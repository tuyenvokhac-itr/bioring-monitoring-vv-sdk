from io import BytesIO

from kaitaistruct import KaitaiStream

from psoc6_dfu.src.cyacd2_file import Cyacd2File
from psoc6_dfu.src.cychecksum import cy_checksum_packet
from psoc6_dfu.src.psoc6_dfu_command_packet import Psoc6DfuCommandPacket


class DfuUtils:
    @staticmethod
    def __checksum( packet: Psoc6DfuCommandPacket):
        # Calculate checksum of the packet
        packet.checksum = cy_checksum_packet(
            packet._io.to_byte_array(), packet.len_data
        )
        # Update checksum field in the packet
        packet._io.seek(4 + packet.len_data)
        packet._io.write_u2le(packet.checksum)

    @staticmethod
    def __build_cmd( packet: Psoc6DfuCommandPacket) -> Psoc6DfuCommandPacket:
        packet.checksum = 0
        packet._check()
        packet._write()
        DfuUtils.__checksum(packet)
        return packet

    @staticmethod
    def build_cmd_enter_dfu():
        ENTER_DFU_PACKET_LENGTH = 11
        cmd_pkt = Psoc6DfuCommandPacket(
            _io=KaitaiStream(BytesIO(bytearray(ENTER_DFU_PACKET_LENGTH)))
        )
        cmd_pkt.command = Psoc6DfuCommandPacket.DfuCommand.enter
        cmd_pkt.len_data = 4
        cmd_pkt.data = Psoc6DfuCommandPacket.ProductId(
            _parent=cmd_pkt, _root=cmd_pkt._root
        )
        cmd_pkt.data.magic = b"\x04\x03\x02\x01"
        return DfuUtils.__build_cmd(cmd_pkt)

    @staticmethod
    def build_cmd_program(address: int, data: bytearray, crc: int):
        data_len = len(data)
        cmd_pkt = Psoc6DfuCommandPacket(
            _io=KaitaiStream(BytesIO(bytearray(data_len + 15)))
        )
        cmd_pkt.command = Psoc6DfuCommandPacket.DfuCommand.program_data
        cmd_pkt.len_data = data_len + 8
        cmd_pkt.data = Psoc6DfuCommandPacket.ProgramData(
            len_data=data_len, _parent=cmd_pkt, _root=cmd_pkt._root
        )
        cmd_pkt.data.address = address
        cmd_pkt.data.crc = crc
        cmd_pkt.data.data = data
        return DfuUtils.__build_cmd(cmd_pkt)

    @staticmethod
    def build_cmd_send_data_no_rsp( data: bytearray):
        data_len = len(data)
        cmd_pkt = Psoc6DfuCommandPacket(
            _io=KaitaiStream(BytesIO(bytearray(data_len + 7)))
        )
        cmd_pkt.command = Psoc6DfuCommandPacket.DfuCommand.send_data_no_resp
        cmd_pkt.len_data = data_len
        cmd_pkt.data = data
        return DfuUtils.__build_cmd(cmd_pkt)

    @staticmethod
    def build_cmd_set_metadata(app_id: int, metadata: Cyacd2File.AppInfo):
        cmd_pkt = Psoc6DfuCommandPacket(_io=KaitaiStream(BytesIO(bytearray(16))))
        cmd_pkt.command = Psoc6DfuCommandPacket.DfuCommand.set_app_metadata
        cmd_pkt.len_data = 9
        cmd_pkt.data = Psoc6DfuCommandPacket.SetAppMetadata(
            _parent=cmd_pkt, _root=cmd_pkt._root
        )
        cmd_pkt.data.app_id = app_id
        cmd_pkt.data.app_metadata = Psoc6DfuCommandPacket.AppMetadata(
            _parent=cmd_pkt.data, _root=cmd_pkt._root
        )
        cmd_pkt.data.app_metadata.start_address = metadata.start_address
        cmd_pkt.data.app_metadata.length = metadata.length
        return DfuUtils.__build_cmd(cmd_pkt)

    @staticmethod
    def build_cmd_with_empty_data(command: Psoc6DfuCommandPacket.DfuCommand):
        EMPTY_PACKET_LENGTH = 7
        cmd_pkt = Psoc6DfuCommandPacket(
            _io=KaitaiStream(BytesIO(bytearray(EMPTY_PACKET_LENGTH)))
        )
        cmd_pkt.command = command
        cmd_pkt.len_data = 0
        cmd_pkt.data = Psoc6DfuCommandPacket.EmptyData(
            _parent=cmd_pkt, _root=cmd_pkt._root
        )
        return DfuUtils.__build_cmd(cmd_pkt)