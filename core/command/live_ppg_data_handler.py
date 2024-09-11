from ...proto import brp_pb2 as brp
import brp_protocol

class LivePpgDataHandler:
    @staticmethod
    def send(isStart = True):
        cid = brp.CommandId.CID_STREAMING_DATA_START
        
        