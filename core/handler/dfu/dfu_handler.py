from typing import Callable, Any, Awaitable

from bleak import BleakClient

from errors.common_result import CommonResult


class DfuHandler:
    def __init__(
            self,
            dfu_file_path: str,
            client: BleakClient,
            write_char: Callable[[BleakClient, str, Any], Awaitable[None]],
            on_dfu_success: Callable[[CommonResult], None],
    ):
        self.dfu_file_path = dfu_file_path
        self.client = client
        self.on_dfu_success = on_dfu_success

    def scan_dfu_devices(self):
        pass

    def connect_dfu_device(self):
        pass

    def subscribe_dfu_characteristics(self):
        pass

    def send_dfu_command_enter(self):
        # Receive response or try 3 times
        # if failed, disconnect and restart dfu process
        pass

    def send_dfu_file(self):
        # reading cyacd2 file
        # loop every row
        # send data no rsp
        # send program data
        # receive response (if program data failed, disconnect and restart the flow)
        # send set meta data
        # send exit dfu mode
        # disconnect device
        pass
