from core.models import TempData

class TempDataHandler:
    @staticmethod
    def handle(data: bytearray) -> TempData:
        return TempDataHandler._parse(data)
    
    @staticmethod
    def _parse(data: bytearray) -> TempData:
        pass