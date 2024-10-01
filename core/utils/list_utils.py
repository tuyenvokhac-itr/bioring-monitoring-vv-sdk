from typing import List, Optional

from core.callbacks.response_callback import ResponseCallback


class ListUtils:
    @staticmethod
    def get_response_callback(response_callbacks: List[ResponseCallback], sid: int) -> Optional[ResponseCallback]:
        return next((callback for callback in response_callbacks if callback.sid == sid), None)
