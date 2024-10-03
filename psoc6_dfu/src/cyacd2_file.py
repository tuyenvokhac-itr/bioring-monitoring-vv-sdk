# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# record_type: ignore

import kaitaistruct
from kaitaistruct import ReadWriteKaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

from psoc6_dfu.src import HexString
class Cyacd2File(ReadWriteKaitaiStruct):
    def __init__(self, _io=None, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self

    def _read(self):
        self.header = Cyacd2File.Header(self._io, self, self._root)
        self.header._read()
        self.app_info = Cyacd2File.AppInfo(self._io, self, self._root)
        self.app_info._read()
        self.data_rows = []
        i = 0
        while not self._io.is_eof():
            _t_data_rows = Cyacd2File.DataRow(self._io, self, self._root)
            _t_data_rows._read()
            self.data_rows.append(_t_data_rows)
            i += 1



    def _fetch_instances(self):
        pass
        self.header._fetch_instances()
        self.app_info._fetch_instances()
        for i in range(len(self.data_rows)):
            pass
            self.data_rows[i]._fetch_instances()



    def _write__seq(self, io=None):
        super(Cyacd2File, self)._write__seq(io)
        self.header._write__seq(self._io)
        self.app_info._write__seq(self._io)
        for i in range(len(self.data_rows)):
            pass
            if self._io.is_eof():
                raise kaitaistruct.ConsistencyError(u"data_rows", self._io.size() - self._io.pos(), 0)
            self.data_rows[i]._write__seq(self._io)

        if not self._io.is_eof():
            raise kaitaistruct.ConsistencyError(u"data_rows", self._io.size() - self._io.pos(), 0)


    def _check(self):
        pass
        if self.header._root != self._root:
            raise kaitaistruct.ConsistencyError(u"header", self.header._root, self._root)
        if self.header._parent != self:
            raise kaitaistruct.ConsistencyError(u"header", self.header._parent, self)
        if self.app_info._root != self._root:
            raise kaitaistruct.ConsistencyError(u"app_info", self.app_info._root, self._root)
        if self.app_info._parent != self:
            raise kaitaistruct.ConsistencyError(u"app_info", self.app_info._parent, self)
        for i in range(len(self.data_rows)):
            pass
            if self.data_rows[i]._root != self._root:
                raise kaitaistruct.ConsistencyError(u"data_rows", self.data_rows[i]._root, self._root)
            if self.data_rows[i]._parent != self:
                raise kaitaistruct.ConsistencyError(u"data_rows", self.data_rows[i]._parent, self)


    class Header(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.header_str = (self._io.read_bytes_term(10, False, True, False)).decode("ASCII")


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Cyacd2File.Header, self)._write__seq(io)
            self._io.write_bytes((self.header_str).encode(u"ASCII"))
            if not self._io.is_eof():
                self._io.write_u1(10)



        def _check(self):
            pass
            if (KaitaiStream.byte_array_index_of((self.header_str).encode(u"ASCII"), 10) != -1):
                raise kaitaistruct.ConsistencyError(u"header_str", KaitaiStream.byte_array_index_of((self.header_str).encode(u"ASCII"), 10), -1)

        @property
        def app_id(self):
            if hasattr(self, '_m_app_id'):
                return self._m_app_id

            self._m_app_id = int((self.header_str)[14:16], 16)
            return getattr(self, '_m_app_id', None)

        def _invalidate_app_id(self):
            del self._m_app_id
        @property
        def product_id(self):
            if hasattr(self, '_m_product_id'):
                return self._m_product_id

            self._m_product_id = int((self.header_str)[16:25], 16)
            return getattr(self, '_m_product_id', None)

        def _invalidate_product_id(self):
            del self._m_product_id
        @property
        def silicon_rev(self):
            if hasattr(self, '_m_silicon_rev'):
                return self._m_silicon_rev

            self._m_silicon_rev = int((self.header_str)[10:12], 16)
            return getattr(self, '_m_silicon_rev', None)

        def _invalidate_silicon_rev(self):
            del self._m_silicon_rev
        @property
        def file_version(self):
            if hasattr(self, '_m_file_version'):
                return self._m_file_version

            self._m_file_version = int((self.header_str)[0:2], 16)
            return getattr(self, '_m_file_version', None)

        def _invalidate_file_version(self):
            del self._m_file_version
        @property
        def silicon_id(self):
            if hasattr(self, '_m_silicon_id'):
                return self._m_silicon_id

            self._m_silicon_id = int((self.header_str)[2:10], 16)
            return getattr(self, '_m_silicon_id', None)

        def _invalidate_silicon_id(self):
            del self._m_silicon_id
        @property
        def checksum_type(self):
            if hasattr(self, '_m_checksum_type'):
                return self._m_checksum_type

            self._m_checksum_type = int((self.header_str)[12:14], 16)
            return getattr(self, '_m_checksum_type', None)

        def _invalidate_checksum_type(self):
            del self._m_checksum_type

    class AppInfo(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.magic = self._io.read_bytes(9)
            if not (self.magic == b"\x40\x41\x50\x50\x49\x4E\x46\x4F\x3A"):
                raise kaitaistruct.ValidationNotEqualError(b"\x40\x41\x50\x50\x49\x4E\x46\x4F\x3A", self.magic, self._io, u"/types/app_info/seq/0")
            self.start_address_str = (self._io.read_bytes_term(44, False, True, False)).decode("ASCII")
            self.length_str = (self._io.read_bytes_term(10, False, True, False)).decode("ASCII")


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Cyacd2File.AppInfo, self)._write__seq(io)
            self._io.write_bytes(self.magic)
            self._io.write_bytes((self.start_address_str).encode(u"ASCII"))
            if not self._io.is_eof():
                self._io.write_u1(44)

            self._io.write_bytes((self.length_str).encode(u"ASCII"))
            if not self._io.is_eof():
                self._io.write_u1(10)



        def _check(self):
            pass
            if (len(self.magic) != 9):
                raise kaitaistruct.ConsistencyError(u"magic", len(self.magic), 9)
            if not (self.magic == b"\x40\x41\x50\x50\x49\x4E\x46\x4F\x3A"):
                raise kaitaistruct.ValidationNotEqualError(b"\x40\x41\x50\x50\x49\x4E\x46\x4F\x3A", self.magic, None, u"/types/app_info/seq/0")
            if (KaitaiStream.byte_array_index_of((self.start_address_str).encode(u"ASCII"), 44) != -1):
                raise kaitaistruct.ConsistencyError(u"start_address_str", KaitaiStream.byte_array_index_of((self.start_address_str).encode(u"ASCII"), 44), -1)
            if (KaitaiStream.byte_array_index_of((self.length_str).encode(u"ASCII"), 10) != -1):
                raise kaitaistruct.ConsistencyError(u"length_str", KaitaiStream.byte_array_index_of((self.length_str).encode(u"ASCII"), 10), -1)

        @property
        def start_address(self):
            if hasattr(self, '_m_start_address'):
                return self._m_start_address

            self._m_start_address = int(self.start_address_str, 16)
            return getattr(self, '_m_start_address', None)

        def _invalidate_start_address(self):
            del self._m_start_address
        @property
        def length(self):
            if hasattr(self, '_m_length'):
                return self._m_length

            self._m_length = int(self.length_str, 16)
            return getattr(self, '_m_length', None)

        def _invalidate_length(self):
            del self._m_length

    class DataRow(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.header = self._io.read_bytes(1)
            if not (self.header == b"\x3A"):
                raise kaitaistruct.ValidationNotEqualError(b"\x3A", self.header, self._io, u"/types/data_row/seq/0")
            self.address_str = (self._io.read_bytes(8)).decode("ASCII")
            self.data = HexString.HexString(self._io)
            self.data._read()


        def _fetch_instances(self):
            pass
            self.data._fetch_instances()


        def _write__seq(self, io=None):
            super(Cyacd2File.DataRow, self)._write__seq(io)
            self._io.write_bytes(self.header)
            self._io.write_bytes((self.address_str).encode(u"ASCII"))
            self.data._write__seq(self._io)


        def _check(self):
            pass
            if (len(self.header) != 1):
                raise kaitaistruct.ConsistencyError(u"header", len(self.header), 1)
            if not (self.header == b"\x3A"):
                raise kaitaistruct.ValidationNotEqualError(b"\x3A", self.header, None, u"/types/data_row/seq/0")
            if (len((self.address_str).encode(u"ASCII")) != 8):
                raise kaitaistruct.ConsistencyError(u"address_str", len((self.address_str).encode(u"ASCII")), 8)

        @property
        def address_1(self):
            if hasattr(self, '_m_address_1'):
                return self._m_address_1

            self._m_address_1 = int((self.address_str)[2:4], 16)
            return getattr(self, '_m_address_1', None)

        def _invalidate_address_1(self):
            del self._m_address_1
        @property
        def address(self):
            if hasattr(self, '_m_address'):
                return self._m_address

            self._m_address = (((self.address_0 | (self.address_1 << 8)) | (self.address_2 << 16)) | (self.address_3 << 24))
            return getattr(self, '_m_address', None)

        def _invalidate_address(self):
            del self._m_address
        @property
        def address_3(self):
            if hasattr(self, '_m_address_3'):
                return self._m_address_3

            self._m_address_3 = int((self.address_str)[6:8], 16)
            return getattr(self, '_m_address_3', None)

        def _invalidate_address_3(self):
            del self._m_address_3
        @property
        def address_0(self):
            if hasattr(self, '_m_address_0'):
                return self._m_address_0

            self._m_address_0 = int((self.address_str)[0:2], 16)
            return getattr(self, '_m_address_0', None)

        def _invalidate_address_0(self):
            del self._m_address_0
        @property
        def address_2(self):
            if hasattr(self, '_m_address_2'):
                return self._m_address_2

            self._m_address_2 = int((self.address_str)[4:6], 16)
            return getattr(self, '_m_address_2', None)

        def _invalidate_address_2(self):
            del self._m_address_2


