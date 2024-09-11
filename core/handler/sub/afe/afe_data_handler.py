from core.models import AfeData

class AfeDataHandler:
    @staticmethod
    def handle(data: bytearray) -> AfeData:
        return AfeDataHandler._parse(data)
    
    @staticmethod
    def _parse(data: bytearray) -> AfeData:
        pass