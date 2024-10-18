import asyncio
from io import BytesIO
from typing import Callable, Tuple, Optional

from bleak import BleakClient, BLEDevice, AdvertisementData
from kaitaistruct import KaitaiStream

from ble.ble_constant import BleConstant
from ble.ble_manager import BleManager
from errors.common_error import CommonError
from errors.common_result import CommonResult
from logger.custom_logger import logger
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
        
    def _init_cyacd_file(self):
        file = open(self.dfu_file_path, "r")
        file_content = file.read()
        _io = KaitaiStream(BytesIO(file_content.encode("utf-8")))
        cyacd = Cyacd2File(_io)
        cyacd._read()
        self.cyacd = cyacd


    def start(self):
        if self.trial_times > 3:
            self.on_dfu_success(CommonResult(is_success=False, error=CommonError.DFU_ERROR))
        logger.info(f"Start DFU with {self.trial_times} trial times")
        self.trial_times += 1
        self.is_writing_file = False

        # Don't need to scan device at the first time.
        if self.trial_times == 1:
            asyncio.create_task(self._subscribe_dfu_char())
        else:
            asyncio.create_task(self._scan_dfu_devices())

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
            logger.info(f"Found DFU device: {device.name}")
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

    def _on_device_connected(self, client: BleakClient):
        self.client = client
        asyncio.create_task(self._subscribe_dfu_char())

    def _on_device_disconnected(self, client: BleakClient):
        logger.info(f"Device {client.address} disconnected, Restart DFU ...")
        self.start()

    def _on_bluetooth_error(self, address: str, error: CommonError):
        logger.error(f"Bluetooth error: {error.name} on device {address}, Restart DFU ...")
        self.start()

    async def _subscribe_dfu_char(self):
        await self.ble_manager.start_notify(
            BleConstant.BRS_UUID_CHAR_DFU,
            self.client,
            self._on_dfu_characteristics_listener,
        )
        logger.info("Subscribed DFU characteristics")

        await self._send_enter_command()
        logger.info("Sent enter DFU command")

    async def _send_enter_command(self):
        packet_enter = DfuUtils.build_cmd_enter_dfu()
        await self._send_command(packet_enter, True)

    def _on_dfu_characteristics_listener(self, sender, data: bytearray):
        rsp_packet = Psoc6DfuResponsePacket(_io=KaitaiStream(BytesIO(data)))
        rsp_packet._read()
        self._response_handler(rsp_packet)

    def _response_handler(self, pkt: Psoc6DfuResponsePacket):
        print(f"DFU response: {pkt.status_code.name}")
        if pkt.status_code != Psoc6DfuResponsePacket.DfuStatusCode.success:
            logger.error(f"DFU response error: {pkt.status_code.name}, Disconnect device ...")
            asyncio.create_task(self.ble_manager.disconnect(self.client))
            return

        """ Enter dfu response success"""
        if not self.is_writing_file:
            logger.info("Enter DFU success")
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

    async def _start_write_file(self, cyacd: Cyacd2File):
        self.is_writing_file = True
        logger.info("Start writing file ...")

        logger.info("Header: ")
        logger.info(f"  File version: {hex(cyacd.header.file_version)}")
        logger.info(f"  Silicon ID: {hex(cyacd.header.silicon_id)}")
        logger.info(f"  Silicon rev: {hex(cyacd.header.silicon_rev)}")
        logger.info(f"  Checksum type: {hex(cyacd.header.checksum_type)}")
        logger.info(f"  App ID: {hex(cyacd.header.app_id)}")
        logger.info(f"  Product ID: {hex(cyacd.header.product_id)}")
        logger.info("App info: ")
        logger.info(f"  Magic: {cyacd.app_info.magic}")
        logger.info(f"  Start address: {hex(cyacd.app_info.start_address)}")
        logger.info(f"  Length: {hex(cyacd.app_info.length)}")
        logger.info("Data: ")
        logger.info(f"  Number of rows: {len(cyacd.data_rows)}\n")

        # Send DFU file to device
        for row in cyacd.data_rows:
            row_data_len = len(row.data.data_bytes)

            row_address = row.address
            logger.info(
                f"Row : {hex(row_address)} ({row_data_len} bytes)"
            )

            # Send data from 0 to 256 bytes (No Response)
            pp = DfuUtils.build_cmd_send_data_no_rsp(row.data.data_bytes[:256])
            await self._send_command(pp)

            # Send data from 384 to 512 bytes and start programming
            pp_final = DfuUtils.build_cmd_program(
                row_address,
                row.data.data_bytes[256:],
                cy_checksum_data(row.data.data_bytes),
            )

            await self._send_command(pp_final, True)

        logger.info("[DONE] Writing DFU file successfully")
        await self._exit()
        self.on_dfu_success(CommonResult(is_success=True))

    async def _exit(self):
        packet_exit = DfuUtils.build_cmd_with_empty_data(
            Psoc6DfuCommandPacket.DfuCommand.exit
        )
        await self._send_command(packet_exit)

    async def _send_command(self, command: Psoc6DfuCommandPacket, response: bool = False):
        cmd_bytes = command._io.to_byte_array()
        logger.info(f"Sending command: {cmd_bytes}")
        await self.ble_manager.write_char(self.client, BleConstant.BRS_UUID_CHAR_DFU, cmd_bytes, response)
