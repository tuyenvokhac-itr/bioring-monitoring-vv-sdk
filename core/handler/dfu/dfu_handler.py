import asyncio
import time
from io import BytesIO
from typing import Callable, Tuple, Optional

from bleak import BleakClient, BLEDevice, AdvertisementData
from kaitaistruct import KaitaiStream

from ble.ble_constant import BleConstant
from ble.ble_manager import BleManager
from errors.common_error import CommonError
from errors.common_result import CommonResult
from psoc6_dfu.src.cyacd2_file import Cyacd2File
from psoc6_dfu.src.cychecksum import cy_checksum_data
from psoc6_dfu.src.dfu_utils import DfuUtils
from psoc6_dfu.src.psoc6_dfu_command_packet import Psoc6DfuCommandPacket
from psoc6_dfu.src.psoc6_dfu_response_packet import Psoc6DfuResponsePacket


class DfuHandler:
    def __init__(
            self,
            device: Tuple[BLEDevice, AdvertisementData],
            client: BleakClient,
            dfu_file_path: str,
            on_dfu_result: Callable[[CommonResult], None],
    ):
        self.dfu_file_path = dfu_file_path
        self.device = device
        self.client = client
        self.on_dfu_success = on_dfu_result

        self.ble_manager = BleManager()
        self.is_writing_file = False
        self.cyacd: Optional[Cyacd2File] = None
        self.trial_times = 0
        self.device_found = False

        self._init_cyacd_file()

    def start(self):
        if self.trial_times > 3:
            self.on_dfu_success(CommonResult(is_success=False, error=CommonError.DFU_ERROR))

        self.trial_times += 1
        asyncio.create_task(self._subscribe_dfu_char())
        # asyncio.create_task(self._scan_dfu_devices())

    async def _scan_dfu_devices(self):
        self.device_found = False
        await self.ble_manager.disconnect(self.client)
        await self.ble_manager.stop_scan()
        await self.ble_manager.start_scan(self._on_device_found)

    def _on_device_found(self, device: BLEDevice, advertisement_data: AdvertisementData):
        if self.device_found is True:
            return

        if device.address == self.device[0].address:
            self.device_found = True
            print(f"Found DFU device: {device.name}")
            asyncio.create_task(self.connect_dfu_device())

    async def connect_dfu_device(self):
        await self.ble_manager.stop_scan()
        await self.ble_manager.connect(
            self.client.address,
            10,
            self._on_device_connected,
            self._on_device_disconnected,
            self._on_bluetooth_error,
        )

    def disconnect_dfu_device(self):
        asyncio.create_task(self.ble_manager.disconnect(self.client))

    def _on_device_connected(self, client: BleakClient):
        self.client = client
        print('connected')
        asyncio.create_task(self._subscribe_dfu_char())

    def _on_device_disconnected(self, client: BleakClient):
        print('disconnected')
        self.start()

    def _on_bluetooth_error(self, address: str, error: CommonError):
        print(f"Bluetooth error: {error}")
        self.start()

    async def _subscribe_dfu_char(self):
        await self.ble_manager.start_notify(
            BleConstant.BRS_UUID_CHAR_DFU,
            self.client,
            self._on_dfu_characteristics_listener,
        )

        await self._send_enter_command()

    async def _send_enter_command(self):
        packet_enter = DfuUtils.build_cmd_enter_dfu()
        await self._send_command(packet_enter, True)

    def _on_dfu_characteristics_listener(self, sender, data: bytearray):
        print(data)
        rsp_packet = Psoc6DfuResponsePacket(_io=KaitaiStream(BytesIO(data)))
        rsp_packet._read()
        self._response_handler(rsp_packet)

    def _response_handler(self, pkt: Psoc6DfuResponsePacket):
        print(pkt)
        if pkt.status_code != Psoc6DfuResponsePacket.DfuStatusCode.success:
            self.disconnect_dfu_device()
            return

        """ Enter dfu response success"""
        if not self.is_writing_file:
            asyncio.create_task(self._on_enter_dfu_success())
            return

        """ Program data success """

    async def _on_enter_dfu_success(self):
        await self._set_metadata(self.cyacd)
        await self._start_write_file(self.cyacd)

    async def _set_metadata(self, dfu_file: Cyacd2File):
        packet_set_app_metadata = DfuUtils.build_cmd_set_metadata(
            dfu_file.header.app_id, dfu_file.app_info
        )
        await self._send_command(packet_set_app_metadata)

    def _init_cyacd_file(self):
        file = open(self.dfu_file_path, "r")
        file_content = file.read()
        _io = KaitaiStream(BytesIO(file_content.encode("utf-8")))
        cyacd = Cyacd2File(_io)
        cyacd._read()
        self.cyacd = cyacd

    async def _start_write_file(self, cyacd : Cyacd2File):
        self.is_writing_file = True

        # Print DFU file info
        print("Header: ")
        print(f"  File version: {hex(cyacd.header.file_version)}")
        print(f"  Silicon ID: {hex(cyacd.header.silicon_id)}")
        print(f"  Silicon rev: {hex(cyacd.header.silicon_rev)}")
        print(f"  Checksum type: {hex(cyacd.header.checksum_type)}")
        print(f"  App ID: {hex(cyacd.header.app_id)}")
        print(f"  Product ID: {hex(cyacd.header.product_id)}")
        print("App info: ")
        print(f"  Magic: {cyacd.app_info.magic}")
        print(f"  Start address: {hex(cyacd.app_info.start_address)}")
        print(f"  Length: {hex(cyacd.app_info.length)}")
        print("Data: ")
        print(f"  Number of rows: {len(cyacd.data_rows)}\n")

        # Send DFU file to device
        for row in cyacd.data_rows:
            row_data_len = len(row.data.data_bytes)

            row_address = row.address
            print(
                f"Row : {hex(row_address)} ({row_data_len} bytes)"
            )

            # Send data from 0 to 256 bytes (No Response)
            pp = DfuUtils.build_cmd_send_data_no_rsp(row.data.data_bytes[:256])
            await self._send_command(pp)
            print("Sent 256 bytes")
            # Send data from 384 to 512 bytes and start programming
            pp_final = DfuUtils.build_cmd_program(
                row_address,
                row.data.data_bytes[256:],
                cy_checksum_data(row.data.data_bytes),
            )

            await self._send_command(pp_final, True)

        await self._exit()
        self.on_dfu_success(CommonResult(is_success=True))
        self.disconnect_dfu_device()


    async def _exit(self):
        packet_exit = DfuUtils.build_cmd_with_empty_data(
            Psoc6DfuCommandPacket.DfuCommand.exit
        )
        await self._send_command(packet_exit)

    async def _send_command(self, command: Psoc6DfuCommandPacket, response: bool = False):
        cmd_bytes = command._io.to_byte_array()
        print(f"Sending command: {cmd_bytes}")
        await self.ble_manager.write_char(self.client, BleConstant.BRS_UUID_CHAR_DFU, cmd_bytes, response)
