from datetime import datetime


class TimeUtil:
    @staticmethod
    def from_epoch_to_ymdhms(epoch: int):
        return datetime.fromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S')
