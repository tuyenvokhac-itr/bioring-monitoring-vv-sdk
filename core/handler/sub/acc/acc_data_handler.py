from core.models import AccData

class AccDataHandler:
    @staticmethod
    def handle(data: bytearray) -> AccData:
        return AccDataHandler._parse(data)
    
    @staticmethod
    def _parse(data: bytearray) -> AccData:
        pass