from core.models import AccData

# PPG and ECG
class AfeDataHandler:
    @staticmethod
    def handle(data: bytearray) -> AccData:
        return AfeDataHandler._parse(data)
    
    @staticmethod
    def _parse(data: bytearray) -> AccData:
        pass