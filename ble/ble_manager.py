import platform
from typing import Callable

from bleak import BleakClient, BleakError
from bleak import BleakScanner, BLEDevice, AdvertisementData

from ble.ble_constant import BleConstant
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
            service_uuids=[BleConstant.BRS_UUID_SERVICE]
        )

        await self.scanner.start()
        print('scanned')

    async def stop_scan(self):
        if self.scanner is not None:
            await self.scanner.stop()

    async def connect(
            self,
            address,
            timeout,
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
        except BleakError as e:
            print(f"BleakError occurred: {e}")
            # Access platform-specific error codes if available
            if hasattr(e, 'hresult'):
                print(f"HRESULT Error Code: {e.hresult}")
            on_bluetooth_error(address, CommonError.CONNECTION_FAILED)
        except Exception as e:
            print(e)
            on_bluetooth_error(address, CommonError.CONNECTION_FAILED)

    async def disconnect(self, client: BleakClient):
        await client.disconnect()

    def get_characteristic_by_uuid(self, char_uuid, client: BleakClient):
        """
        Get the BleakGATTCharacteristic object based on the provided characteristic UUID.
        """
        for service in client.services:
            for characteristic in service.characteristics:
                if characteristic.uuid == char_uuid:
                    return characteristic
        return None

    async def start_notify(self, char_uuid: str, client: BleakClient, callback):
        """
        Start receiving notifications for the specified characteristic UUID.
        """
        characteristic = self.get_characteristic_by_uuid(char_uuid, client)
        if characteristic:
            await client.start_notify(characteristic, callback)

    async def write_char(self, client: BleakClient, char_uuid: str, value, response=True):
        """
        Write value to the specified characteristic UUID.
        """
        characteristic = self.get_characteristic_by_uuid(char_uuid, client)
        if characteristic:
            await client.write_gatt_char(characteristic, value, response)
