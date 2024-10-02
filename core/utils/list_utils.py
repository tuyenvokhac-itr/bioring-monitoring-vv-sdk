from typing import List, Optional

from core.callbacks.response_callback import ResponseCallback
from core.callbacks.streaming_callback import StreamingCallback
from core.enum.sensor_type import SensorType


class ListUtils:
    @staticmethod
    def get_response_callback(response_callbacks: List[ResponseCallback], sid: int) -> Optional[ResponseCallback]:
        return next((callback for callback in response_callbacks if callback.sid == sid), None)

    @staticmethod
    def get_streaming_callbacks(
            streaming_callbacks: List[StreamingCallback],
            sensor_type: SensorType
    ) -> List[StreamingCallback]:
        return [
            callback for callback in streaming_callbacks if
            callback.sensor_type == sensor_type
        ]
