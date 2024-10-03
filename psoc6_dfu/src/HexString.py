
import kaitaistruct
from kaitaistruct import ReadWriteKaitaiStruct, KaitaiStream, BytesIO

class HexString(ReadWriteKaitaiStruct):
    def __init__(self, _io=None, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root

    def _read(self):
        self.data_str = (self._io.read_bytes_term(10, False, True, False)).decode("ASCII")
        self.data_bytes = bytes.fromhex(self.data_str)

    def __len__(self):
        return len(self.data_bytes)