# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# record_type: ignore

import kaitaistruct
from kaitaistruct import ReadWriteKaitaiStruct, KaitaiStream, BytesIO
from enum import IntEnum
from psoc6_dfu.src import cychecksum

if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Psoc6DfuResponsePacket(ReadWriteKaitaiStruct):

    class DfuStatusCode(IntEnum):
        success = 0
        error_verify = 2
        error_length = 3
        error_data = 4
        error_cmd = 5
        error_checksum = 8
        error_row = 10
        error_row_access = 11
        error_unknown = 15
    def __init__(self, _io=None, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self

    def _read(self):
        self.sop = self._io.read_bytes(1)
        if not (self.sop == b"\x01"):
            raise kaitaistruct.ValidationNotEqualError(b"\x01", self.sop, self._io, u"/seq/0")
        self.status_code = KaitaiStream.resolve_enum(Psoc6DfuResponsePacket.DfuStatusCode, self._io.read_u1())
        self.len_data = self._io.read_u2le()
        self.data = self._io.read_bytes(self.len_data)
        self.checksum = self._io.read_u2le()
        calculated_checksum = cychecksum.cy_checksum_packet(self._io.to_byte_array(), self.len_data)
        if self.checksum != calculated_checksum:
            raise kaitaistruct.ValidationNotEqualError(calculated_checksum, self.checksum, self._io, u"/seq/4")
        self.eop = self._io.read_bytes(1)
        if not (self.eop == b"\x17"):
            raise kaitaistruct.ValidationNotEqualError(b"\x17", self.eop, self._io, u"/seq/5")


    def _fetch_instances(self):
        pass


    def _write__seq(self, io=None):
        super(Psoc6DfuResponsePacket, self)._write__seq(io)
        self._io.write_bytes(self.sop)
        self._io.write_u1(int(self.status_code))
        self._io.write_u2le(self.len_data)
        self._io.write_bytes(self.data)
        self._io.write_u2le(self.checksum)
        self._io.write_bytes(self.eop)


    def _check(self):
        pass
        if (len(self.sop) != 1):
            raise kaitaistruct.ConsistencyError(u"sop", len(self.sop), 1)
        if not (self.sop == b"\x01"):
            raise kaitaistruct.ValidationNotEqualError(b"\x01", self.sop, None, u"/seq/0")
        if (len(self.data) != self.len_data):
            raise kaitaistruct.ConsistencyError(u"data", len(self.data), self.len_data)
        if (len(self.eop) != 1):
            raise kaitaistruct.ConsistencyError(u"eop", len(self.eop), 1)
        if not (self.eop == b"\x17"):
            raise kaitaistruct.ValidationNotEqualError(b"\x17", self.eop, None, u"/seq/5")

    class EnterResponse(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.silicon_id = self._io.read_u4le()
            self.silicon_rev = self._io.read_u1()
            self.dfu_sdk_version = self._io.read_bytes(3)


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Psoc6DfuResponsePacket.EnterResponse, self)._write__seq(io)
            self._io.write_u4le(self.silicon_id)
            self._io.write_u1(self.silicon_rev)
            self._io.write_bytes(self.dfu_sdk_version)


        def _check(self):
            pass
            if (len(self.dfu_sdk_version) != 3):
                raise kaitaistruct.ConsistencyError(u"dfu_sdk_version", len(self.dfu_sdk_version), 3)



