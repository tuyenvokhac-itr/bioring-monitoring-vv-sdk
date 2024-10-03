# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# record_type: ignore

import kaitaistruct
from kaitaistruct import ReadWriteKaitaiStruct, KaitaiStream, BytesIO
from enum import IntEnum


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Psoc6DfuCommandPacket(ReadWriteKaitaiStruct):

    class DfuCommand(IntEnum):
        verify_app = 49
        sync = 53
        send_data = 55
        enter = 56
        exit = 59
        get_metadata = 60
        erase_data = 68
        send_data_no_resp = 71
        program_data = 73
        verify_data = 74
        set_app_metadata = 76
        set_eivector = 77
    def __init__(self, _io=None, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self.sop = b'\x01'
        self.eop = b'\x17'

    def _read(self):
        self.sop = self._io.read_bytes(1)
        if not (self.sop == b"\x01"):
            raise kaitaistruct.ValidationNotEqualError(b"\x01", self.sop, self._io, u"/seq/0")
        self.command = KaitaiStream.resolve_enum(Psoc6DfuCommandPacket.DfuCommand, self._io.read_u1())
        self.len_data = self._io.read_u2le()
        _on = self.command
        if _on == Psoc6DfuCommandPacket.DfuCommand.verify_data:
            pass
            self._raw_data = self._io.read_bytes(self.len_data)
            _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
            self.data = Psoc6DfuCommandPacket.VerifyData((self.len_data - 8), _io__raw_data, self, self._root)
            self.data._read()
        elif _on == Psoc6DfuCommandPacket.DfuCommand.set_app_metadata:
            pass
            self._raw_data = self._io.read_bytes(self.len_data)
            _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
            self.data = Psoc6DfuCommandPacket.SetAppMetadata(_io__raw_data, self, self._root)
            self.data._read()
        elif _on == Psoc6DfuCommandPacket.DfuCommand.program_data:
            pass
            self._raw_data = self._io.read_bytes(self.len_data)
            _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
            self.data = Psoc6DfuCommandPacket.ProgramData((self.len_data - 8), _io__raw_data, self, self._root)
            self.data._read()
        elif _on == Psoc6DfuCommandPacket.DfuCommand.get_metadata:
            pass
            self._raw_data = self._io.read_bytes(self.len_data)
            _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
            self.data = Psoc6DfuCommandPacket.GetMetadata(_io__raw_data, self, self._root)
            self.data._read()
        elif _on == Psoc6DfuCommandPacket.DfuCommand.sync:
            pass
            self._raw_data = self._io.read_bytes(self.len_data)
            _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
            self.data = Psoc6DfuCommandPacket.EmptyData(_io__raw_data, self, self._root)
            self.data._read()
        elif _on == Psoc6DfuCommandPacket.DfuCommand.erase_data:
            pass
            self._raw_data = self._io.read_bytes(self.len_data)
            _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
            self.data = Psoc6DfuCommandPacket.EraseData(_io__raw_data, self, self._root)
            self.data._read()
        elif _on == Psoc6DfuCommandPacket.DfuCommand.enter:
            pass
            self._raw_data = self._io.read_bytes(self.len_data)
            _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
            self.data = Psoc6DfuCommandPacket.ProductId(_io__raw_data, self, self._root)
            self.data._read()
        elif _on == Psoc6DfuCommandPacket.DfuCommand.exit:
            pass
            self._raw_data = self._io.read_bytes(self.len_data)
            _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
            self.data = Psoc6DfuCommandPacket.EmptyData(_io__raw_data, self, self._root)
            self.data._read()
        elif _on == Psoc6DfuCommandPacket.DfuCommand.verify_app:
            pass
            self.data = self._io.read_u1()
        else:
            pass
            self.data = self._io.read_bytes(self.len_data)
        self.checksum = self._io.read_u2le()
        self.eop = self._io.read_bytes(1)
        if not (self.eop == b"\x17"):
            raise kaitaistruct.ValidationNotEqualError(b"\x17", self.eop, self._io, u"/seq/5")


    def _fetch_instances(self):
        pass
        _on = self.command
        if _on == Psoc6DfuCommandPacket.DfuCommand.verify_data:
            pass
            self.data._fetch_instances()
        elif _on == Psoc6DfuCommandPacket.DfuCommand.set_app_metadata:
            pass
            self.data._fetch_instances()
        elif _on == Psoc6DfuCommandPacket.DfuCommand.program_data:
            pass
            self.data._fetch_instances()
        elif _on == Psoc6DfuCommandPacket.DfuCommand.get_metadata:
            pass
            self.data._fetch_instances()
        elif _on == Psoc6DfuCommandPacket.DfuCommand.sync:
            pass
            self.data._fetch_instances()
        elif _on == Psoc6DfuCommandPacket.DfuCommand.erase_data:
            pass
            self.data._fetch_instances()
        elif _on == Psoc6DfuCommandPacket.DfuCommand.enter:
            pass
            self.data._fetch_instances()
        elif _on == Psoc6DfuCommandPacket.DfuCommand.exit:
            pass
            self.data._fetch_instances()
        elif _on == Psoc6DfuCommandPacket.DfuCommand.verify_app:
            pass
        else:
            pass


    def _write__seq(self, io=None):
        super(Psoc6DfuCommandPacket, self)._write__seq(io)
        self._io.write_bytes(self.sop)
        self._io.write_u1(int(self.command))
        self._io.write_u2le(self.len_data)
        _on = self.command
        if _on == Psoc6DfuCommandPacket.DfuCommand.verify_data:
            pass
            _io__raw_data = KaitaiStream(BytesIO(bytearray(self.len_data)))
            self._io.add_child_stream(_io__raw_data)
            _pos2 = self._io.pos()
            self._io.seek(self._io.pos() + (self.len_data))
            def handler(parent, _io__raw_data=_io__raw_data):
                self._raw_data = _io__raw_data.to_byte_array()
                if (len(self._raw_data) != self.len_data):
                    raise kaitaistruct.ConsistencyError(u"raw(data)", len(self._raw_data), self.len_data)
                parent.write_bytes(self._raw_data)
            _io__raw_data.write_back_handler = KaitaiStream.WriteBackHandler(_pos2, handler)
            self.data._write__seq(_io__raw_data)
        elif _on == Psoc6DfuCommandPacket.DfuCommand.set_app_metadata:
            pass
            _io__raw_data = KaitaiStream(BytesIO(bytearray(self.len_data)))
            self._io.add_child_stream(_io__raw_data)
            _pos2 = self._io.pos()
            self._io.seek(self._io.pos() + (self.len_data))
            def handler(parent, _io__raw_data=_io__raw_data):
                self._raw_data = _io__raw_data.to_byte_array()
                if (len(self._raw_data) != self.len_data):
                    raise kaitaistruct.ConsistencyError(u"raw(data)", len(self._raw_data), self.len_data)
                parent.write_bytes(self._raw_data)
            _io__raw_data.write_back_handler = KaitaiStream.WriteBackHandler(_pos2, handler)
            self.data._write__seq(_io__raw_data)
        elif _on == Psoc6DfuCommandPacket.DfuCommand.program_data:
            pass
            _io__raw_data = KaitaiStream(BytesIO(bytearray(self.len_data)))
            self._io.add_child_stream(_io__raw_data)
            _pos2 = self._io.pos()
            self._io.seek(self._io.pos() + (self.len_data))
            def handler(parent, _io__raw_data=_io__raw_data):
                self._raw_data = _io__raw_data.to_byte_array()
                if (len(self._raw_data) != self.len_data):
                    raise kaitaistruct.ConsistencyError(u"raw(data)", len(self._raw_data), self.len_data)
                parent.write_bytes(self._raw_data)
            _io__raw_data.write_back_handler = KaitaiStream.WriteBackHandler(_pos2, handler)
            self.data._write__seq(_io__raw_data)
        elif _on == Psoc6DfuCommandPacket.DfuCommand.get_metadata:
            pass
            _io__raw_data = KaitaiStream(BytesIO(bytearray(self.len_data)))
            self._io.add_child_stream(_io__raw_data)
            _pos2 = self._io.pos()
            self._io.seek(self._io.pos() + (self.len_data))
            def handler(parent, _io__raw_data=_io__raw_data):
                self._raw_data = _io__raw_data.to_byte_array()
                if (len(self._raw_data) != self.len_data):
                    raise kaitaistruct.ConsistencyError(u"raw(data)", len(self._raw_data), self.len_data)
                parent.write_bytes(self._raw_data)
            _io__raw_data.write_back_handler = KaitaiStream.WriteBackHandler(_pos2, handler)
            self.data._write__seq(_io__raw_data)
        elif _on == Psoc6DfuCommandPacket.DfuCommand.sync:
            pass
            _io__raw_data = KaitaiStream(BytesIO(bytearray(self.len_data)))
            self._io.add_child_stream(_io__raw_data)
            _pos2 = self._io.pos()
            self._io.seek(self._io.pos() + (self.len_data))
            def handler(parent, _io__raw_data=_io__raw_data):
                self._raw_data = _io__raw_data.to_byte_array()
                if (len(self._raw_data) != self.len_data):
                    raise kaitaistruct.ConsistencyError(u"raw(data)", len(self._raw_data), self.len_data)
                parent.write_bytes(self._raw_data)
            _io__raw_data.write_back_handler = KaitaiStream.WriteBackHandler(_pos2, handler)
            self.data._write__seq(_io__raw_data)
        elif _on == Psoc6DfuCommandPacket.DfuCommand.erase_data:
            pass
            _io__raw_data = KaitaiStream(BytesIO(bytearray(self.len_data)))
            self._io.add_child_stream(_io__raw_data)
            _pos2 = self._io.pos()
            self._io.seek(self._io.pos() + (self.len_data))
            def handler(parent, _io__raw_data=_io__raw_data):
                self._raw_data = _io__raw_data.to_byte_array()
                if (len(self._raw_data) != self.len_data):
                    raise kaitaistruct.ConsistencyError(u"raw(data)", len(self._raw_data), self.len_data)
                parent.write_bytes(self._raw_data)
            _io__raw_data.write_back_handler = KaitaiStream.WriteBackHandler(_pos2, handler)
            self.data._write__seq(_io__raw_data)
        elif _on == Psoc6DfuCommandPacket.DfuCommand.enter:
            pass
            _io__raw_data = KaitaiStream(BytesIO(bytearray(self.len_data)))
            self._io.add_child_stream(_io__raw_data)
            _pos2 = self._io.pos()
            self._io.seek(self._io.pos() + (self.len_data))
            def handler(parent, _io__raw_data=_io__raw_data):
                self._raw_data = _io__raw_data.to_byte_array()
                if (len(self._raw_data) != self.len_data):
                    raise kaitaistruct.ConsistencyError(u"raw(data)", len(self._raw_data), self.len_data)
                parent.write_bytes(self._raw_data)
            _io__raw_data.write_back_handler = KaitaiStream.WriteBackHandler(_pos2, handler)
            self.data._write__seq(_io__raw_data)
        elif _on == Psoc6DfuCommandPacket.DfuCommand.exit:
            pass
            _io__raw_data = KaitaiStream(BytesIO(bytearray(self.len_data)))
            self._io.add_child_stream(_io__raw_data)
            _pos2 = self._io.pos()
            self._io.seek(self._io.pos() + (self.len_data))
            def handler(parent, _io__raw_data=_io__raw_data):
                self._raw_data = _io__raw_data.to_byte_array()
                if (len(self._raw_data) != self.len_data):
                    raise kaitaistruct.ConsistencyError(u"raw(data)", len(self._raw_data), self.len_data)
                parent.write_bytes(self._raw_data)
            _io__raw_data.write_back_handler = KaitaiStream.WriteBackHandler(_pos2, handler)
            self.data._write__seq(_io__raw_data)
        elif _on == Psoc6DfuCommandPacket.DfuCommand.verify_app:
            pass
            self._io.write_u1(self.data)
        else:
            pass
            self._io.write_bytes(self.data)
        self._io.write_u2le(self.checksum)
        self._io.write_bytes(self.eop)


    def _check(self):
        pass
        if (len(self.sop) != 1):
            raise kaitaistruct.ConsistencyError(u"sop", len(self.sop), 1)
        if not (self.sop == b"\x01"):
            raise kaitaistruct.ValidationNotEqualError(b"\x01", self.sop, None, u"/seq/0")
        _on = self.command
        if _on == Psoc6DfuCommandPacket.DfuCommand.verify_data:
            pass
            if self.data._root != self._root:
                raise kaitaistruct.ConsistencyError(u"data", self.data._root, self._root)
            if self.data._parent != self:
                raise kaitaistruct.ConsistencyError(u"data", self.data._parent, self)
            if (self.data.len_data != (self.len_data - 8)):
                raise kaitaistruct.ConsistencyError(u"data", self.data.len_data, (self.len_data - 8))
        elif _on == Psoc6DfuCommandPacket.DfuCommand.set_app_metadata:
            pass
            if self.data._root != self._root:
                raise kaitaistruct.ConsistencyError(u"data", self.data._root, self._root)
            if self.data._parent != self:
                raise kaitaistruct.ConsistencyError(u"data", self.data._parent, self)
        elif _on == Psoc6DfuCommandPacket.DfuCommand.program_data:
            pass
            if self.data._root != self._root:
                raise kaitaistruct.ConsistencyError(u"data", self.data._root, self._root)
            if self.data._parent != self:
                raise kaitaistruct.ConsistencyError(u"data", self.data._parent, self)
            if (self.data.len_data != (self.len_data - 8)):
                raise kaitaistruct.ConsistencyError(u"data", self.data.len_data, (self.len_data - 8))
        elif _on == Psoc6DfuCommandPacket.DfuCommand.get_metadata:
            pass
            if self.data._root != self._root:
                raise kaitaistruct.ConsistencyError(u"data", self.data._root, self._root)
            if self.data._parent != self:
                raise kaitaistruct.ConsistencyError(u"data", self.data._parent, self)
        elif _on == Psoc6DfuCommandPacket.DfuCommand.sync:
            pass
            if self.data._root != self._root:
                raise kaitaistruct.ConsistencyError(u"data", self.data._root, self._root)
            if self.data._parent != self:
                raise kaitaistruct.ConsistencyError(u"data", self.data._parent, self)
        elif _on == Psoc6DfuCommandPacket.DfuCommand.erase_data:
            pass
            if self.data._root != self._root:
                raise kaitaistruct.ConsistencyError(u"data", self.data._root, self._root)
            if self.data._parent != self:
                raise kaitaistruct.ConsistencyError(u"data", self.data._parent, self)
        elif _on == Psoc6DfuCommandPacket.DfuCommand.enter:
            pass
            if self.data._root != self._root:
                raise kaitaistruct.ConsistencyError(u"data", self.data._root, self._root)
            if self.data._parent != self:
                raise kaitaistruct.ConsistencyError(u"data", self.data._parent, self)
        elif _on == Psoc6DfuCommandPacket.DfuCommand.exit:
            pass
            if self.data._root != self._root:
                raise kaitaistruct.ConsistencyError(u"data", self.data._root, self._root)
            if self.data._parent != self:
                raise kaitaistruct.ConsistencyError(u"data", self.data._parent, self)
        elif _on == Psoc6DfuCommandPacket.DfuCommand.verify_app:
            pass
        else:
            pass
            if (len(self.data) != self.len_data):
                raise kaitaistruct.ConsistencyError(u"data", len(self.data), self.len_data)
        if (len(self.eop) != 1):
            raise kaitaistruct.ConsistencyError(u"eop", len(self.eop), 1)
        if not (self.eop == b"\x17"):
            raise kaitaistruct.ValidationNotEqualError(b"\x17", self.eop, None, u"/seq/5")

    class SetAppMetadata(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.app_id = self._io.read_u1()
            self.app_metadata = Psoc6DfuCommandPacket.AppMetadata(self._io, self, self._root)
            self.app_metadata._read()


        def _fetch_instances(self):
            pass
            self.app_metadata._fetch_instances()


        def _write__seq(self, io=None):
            super(Psoc6DfuCommandPacket.SetAppMetadata, self)._write__seq(io)
            self._io.write_u1(self.app_id)
            self.app_metadata._write__seq(self._io)


        def _check(self):
            pass
            if self.app_metadata._root != self._root:
                raise kaitaistruct.ConsistencyError(u"app_metadata", self.app_metadata._root, self._root)
            if self.app_metadata._parent != self:
                raise kaitaistruct.ConsistencyError(u"app_metadata", self.app_metadata._parent, self)


    class AppMetadata(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.start_address = self._io.read_u4le()
            self.length = self._io.read_u4le()


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Psoc6DfuCommandPacket.AppMetadata, self)._write__seq(io)
            self._io.write_u4le(self.start_address)
            self._io.write_u4le(self.length)


        def _check(self):
            pass


    class EmptyData(ReadWriteKaitaiStruct):
        """empty_data record_type for commands that don't have data."""
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            pass


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Psoc6DfuCommandPacket.EmptyData, self)._write__seq(io)


        def _check(self):
            pass


    class VerifyData(ReadWriteKaitaiStruct):
        def __init__(self, len_data, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root
            self.len_data = len_data

        def _read(self):
            self.address = self._io.read_u4le()
            self.crc = self._io.read_u4le()
            self.data = self._io.read_bytes(self.len_data)


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Psoc6DfuCommandPacket.VerifyData, self)._write__seq(io)
            self._io.write_u4le(self.address)
            self._io.write_u4le(self.crc)
            self._io.write_bytes(self.data)


        def _check(self):
            pass
            if (len(self.data) != self.len_data):
                raise kaitaistruct.ConsistencyError(u"data", len(self.data), self.len_data)


    class ProductId(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.magic = self._io.read_bytes(4)
            if not (self.magic == b"\x04\x03\x02\x01"):
                raise kaitaistruct.ValidationNotEqualError(b"\x04\x03\x02\x01", self.magic, self._io, u"/types/product_id/seq/0")


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Psoc6DfuCommandPacket.ProductId, self)._write__seq(io)
            self._io.write_bytes(self.magic)


        def _check(self):
            pass
            if (len(self.magic) != 4):
                raise kaitaistruct.ConsistencyError(u"magic", len(self.magic), 4)
            if not (self.magic == b"\x04\x03\x02\x01"):
                raise kaitaistruct.ValidationNotEqualError(b"\x04\x03\x02\x01", self.magic, None, u"/types/product_id/seq/0")


    class ProgramData(ReadWriteKaitaiStruct):
        def __init__(self, len_data, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root
            self.len_data = len_data

        def _read(self):
            self.address = self._io.read_u4le()
            self.crc = self._io.read_u4le()
            self.data = self._io.read_bytes(self.len_data)


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Psoc6DfuCommandPacket.ProgramData, self)._write__seq(io)
            self._io.write_u4le(self.address)
            self._io.write_u4le(self.crc)
            self._io.write_bytes(self.data)


        def _check(self):
            pass
            if (len(self.data) != self.len_data):
                raise kaitaistruct.ConsistencyError(u"data", len(self.data), self.len_data)


    class GetMetadata(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.from_offset = self._io.read_u2le()
            self.to_offset = self._io.read_u2le()


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Psoc6DfuCommandPacket.GetMetadata, self)._write__seq(io)
            self._io.write_u2le(self.from_offset)
            self._io.write_u2le(self.to_offset)


        def _check(self):
            pass


    class EraseData(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.address = self._io.read_u4le()


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Psoc6DfuCommandPacket.EraseData, self)._write__seq(io)
            self._io.write_u4le(self.address)


        def _check(self):
            pass



