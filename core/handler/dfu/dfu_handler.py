import asyncio
import  time
from io import BytesIO
from typing import Callable, Any, Awaitable, Tuple

from bleak import BleakClient, BLEDevice, AdvertisementData
from kaitaistruct import KaitaiStream

from ble.ble_constant import BleConstant
from ble.ble_manager import BleManager
from ble.bt_device import BTDevice
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
            dfu_file_path: str,
            device: Tuple[BLEDevice, AdvertisementData],
            write_char: Callable[[BleakClient, str, Any], Awaitable[None]],
            on_dfu_success: Callable[[CommonResult], None],
    ):
        self.dfu_file_path = dfu_file_path
        self.device = device
        self.client = None
        self.on_dfu_success = on_dfu_success
        self.ble_manager = BleManager()
        self.scan_dfu_devices()

    def scan_dfu_devices(self):
        self.ble_manager.start_scan(self._on_device_found)

    def _on_device_found(self, device: BLEDevice, advertisement_data: AdvertisementData):
        if device.name is not None and BleConstant.BIORING_DFU_PREFIX in device.name:
            # check if device is the device we are looking for
            cut_dfu_device_name = device.name.replace(BleConstant.BIORING_DFU_PREFIX, "", 1)
            cut_device_name = self.device[0].name.replace(BleConstant.BIORING_PREFIX, "", 1)

            if cut_dfu_device_name == cut_device_name:
                self.ble_manager.stop_scan()
                self.ble_manager.connect(
                    self.client.address,
                    10,
                    self._on_device_connected,
                    self._on_device_disconnected,
                    self._on_bluetooth_error,
                )

    def _on_device_connected(self, client: BleakClient):
        self.client = client
        asyncio.create_task(self.start_dfu())

    async def start_dfu(self):
        await self.ble_manager.start_notify(
            BleConstant.BRS_UUID_CHAR_DFU,
            self.client,
            self._on_dfu_characteristics_subscribed,
        )
        await self.start_dfu_program()

    def _on_dfu_characteristics_subscribed(self, sender, data: bytearray):
        rsp_packet = Psoc6DfuResponsePacket(_io=KaitaiStream(BytesIO(data)))
        rsp_packet._read()
        self._response_handler(rsp_packet)

    async def _response_handler(self, pkt: Psoc6DfuResponsePacket):
        if pkt.status_code != Psoc6DfuResponsePacket.DfuStatusCode.success:
            # handle retry or return error.
            pass
        else:
            # handle success
            await self.start_write_file()

    def _on_device_disconnected(self, client: BleakClient):
        pass

    def _on_bluetooth_error(self, address: str, error: CommonError):
        pass

    async def start_dfu_program(self):

        await self.enter_dfu()

    async def enter_dfu(self) -> bool:
        packet_enter = DfuUtils.build_cmd_enter_dfu()
        await self.send_command(packet_enter)
        pass

    async def send_command(self, command: Psoc6DfuCommandPacket) -> bool:
        cmd_bytes = command._io.to_byte_array()
        await self.ble_manager.write_char(self.client, BleConstant.BRS_UUID_CHAR_DFU, cmd_bytes, True)

    async def start_write_file(self):
        file = open(self.dfu_file_path, "r")
        program_start_time = time.time()

        # Read DFU file
        file_content = file.read()
        # Parase DFU file to Cyacd2File object
        _io = KaitaiStream(BytesIO(file_content.encode("utf-8")))
        cyacd = Cyacd2File(_io)
        cyacd._read()
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
        i = 0
        for row in cyacd.data_rows:
            row_data_len = len(row.data.data_bytes)

            row_address = row.address
            print(
                f"Row {i}: {hex(row_address)} ({row_data_len} bytes)"
            )

            # progress_update.dfu_progress_update.emit(i * 100 // len(cyacd.data_rows))

            # Send data from 0 to 256 bytes (No Response)
            pp = DfuUtils.build_cmd_send_data_no_rsp(row.data.data_bytes[:256])
            await self.send_command(pp)

            # Send data from 384 to 512 bytes and start programming
            pp_final = DfuUtils.build_cmd_program(
                row_address,
                row.data.data_bytes[256:],
                cy_checksum_data(row.data.data_bytes),
            )
            rsp_pkt = await self.send_command(pp_final, response=True, retry=0)
            if (
                    rsp_pkt != None
                    and rsp_pkt.status_code
                    != Psoc6DfuResponsePacket.DfuStatusCode.success
            ):
                self.dfu_status = False
                return False

            i = i + 1

        # Finalize programming by setting metadata and send exit packet
        await self.set_metadata(cyacd)
        await self.exit()

    async def set_metadata(self, dfu_file: Cyacd2File) -> bool:
        packet_set_app_metadata = DfuUtils.build_cmd_set_metadata(
            dfu_file.header.app_id, dfu_file.app_info
        )
        await self.send_command(packet_set_app_metadata, response=False)

    async def exit(self):
        packet_exit = DfuUtils.build_cmd_with_empty_data(
            Psoc6DfuCommandPacket.DfuCommand.exit
        )
        await self.send_command(packet_exit, response=False)
        # NOTE: this command is not acknowledged