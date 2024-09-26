from enum import Enum

import proto.brp_pb2 as brp


class LogLevel(Enum):
    ERROR = 0
    WARNING = 1
    DEBUG = 2
    INFO = 3

    def to_brp_log_level(self) -> brp.LogLevel:
        mapping = {
            LogLevel.ERROR: brp.LogLevel.LOG_LEVEL_ERROR,
            LogLevel.WARNING: brp.LogLevel.LOG_LEVEL_WARNING,
            LogLevel.DEBUG: brp.LogLevel.LOG_LEVEL_DEBUG,
            LogLevel.INFO: brp.LogLevel.LOG_LEVEL_INFO,
        }
        return mapping.get(self, None)
