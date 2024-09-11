from proto import brp_pb2 as brp
import brp_protocol

class GetDeviceInfoHandler:
    @staticmethod
    def send():
        cid = brp.CommandId.CID_DEV_INFO_GET
        
        