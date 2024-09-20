import platform
from typing import Callable
from bleak import BleakClient
from bleak import BleakScanner, BLEDevice, AdvertisementData
from errors.common_error import CommonError


class BleManager:
    def __init__(self, debug=False):
        self.scanner = None

        if platform.system() == "Windows":  # Windows
            self.use_bdaddr = True
        else:
            self.use_bdaddr = False

    async def start_scan(self, detection_callback: Callable[[BLEDevice, AdvertisementData], None]):
        self.scanner = BleakScanner(
            cb=dict(use_bdaddr=self.use_bdaddr),
            detection_callback=detection_callback,
            # service_uuids=[BleConstant.BRS_UUID_SERVICE]
        )

        await self.scanner.start()

    async def stop_scan(self):
        if self.scanner:
            await self.scanner.stop()

    async def connect(
            self,
            address, timeout,
            on_device_connected: Callable[[BleakClient], None],
            on_device_disconnected: Callable[[BleakClient], None],
            on_bluetooth_error: Callable[[str, CommonError], None]
    ):
        try:
            client = BleakClient(
                address_or_ble_device=address,
                timeout=timeout,
                disconnected_callback=on_device_disconnected
            )
            await client.connect()
            on_device_connected(client)
        except Exception as e:
            print(e)
            on_bluetooth_error(address, CommonError.CONNECTION_FAILED)

    async def disconnect(self, client: BleakClient):
        await client.disconnect()
