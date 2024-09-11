import asyncio
import queue
from enum import Enum
from threading import Thread, Event
from bleak import BleakScanner
from bleak import BleakClient
import logging
import platform


class BLEConnectionStatus(Enum):
    INIT = 0
    CONNECTING = 1
    CONNECTED = 2
    DISCONNECTED = 3


class BLEEvent(Enum):
    BLE_EVENT_DISCONNECT = 0
    BLE_EVENT_START_NOTIFY = 1
    BLE_EVENT_STOP_NOTIFY = 2
    BLE_EVENT_WRITE = 3


class BLEManagerOld:
    def __init__(self, debug=False):

        self.addr = ""
        self.event_queue = queue.Queue()
        self.conn_status = BLEConnectionStatus.INIT
        self.conn_timeout = False

        if platform.system() == "Darwin":  # macOS
            self.use_bdaddr = False
        elif platform.system() == "Windows":  # Windows
            self.use_bdaddr = True
        else:
            self.use_bdaddr = False  # Linux

    def scan(self):
        """
        Scan for nearby BLE devices.
        """
        devices = asyncio.run(
            BleakScanner.discover(
                return_adv=True, cb=dict(use_bdaddr=self.use_bdaddr), timeout=10
            )
        )
        self.filtered_devices = []
        for d, a in devices.values():
            if d.name != None and "BioRing" in d.name:
                self.filtered_devices.append((d, a))
        return self.filtered_devices

    def scan_dfu(self):
        """
        Scan for nearby DFU BLE devices.
        """
        devices = asyncio.run(BleakScanner.discover())
        self.filtered_devices = []
        for d in devices:
            if d.name != None and "[DFU] BioRing" in d.name:
                self.filtered_devices.append(d)
        return self.filtered_devices

    def connect(self, addr, pairing=False):
        """
        Start the thread for establishing and managing the BLE connection.
        """
        self.addr = addr
        self.pairing = pairing
        self.conn_timeout = False
        self.thread = Thread(target=self.__thread_handler)
        try:
            self.thread.start()
        except:
            self.disconnect()
            self.thread.start()

    def disconnect(self):
        """
        Disconnect from the BLE device.
        Stop the execution of the thread by joining it.
        """
        # self.closed_event.set()
        self.event_queue.put((BLEEvent.BLE_EVENT_DISCONNECT, None))
        if self.connected():
            if self.thread.is_alive():
                self.thread.join()

    def connected(self):
        return self.conn_status == BLEConnectionStatus.CONNECTED

    def start_notify(self, char_uuid, callback):
        """
        Start receiving notifications for the specified characteristic UUID.
        """
        if self.connected():
            characteristic = self.get_characteristic_by_uuid(char_uuid)
            if characteristic:
                self.event_queue.put(
                    (BLEEvent.BLE_EVENT_START_NOTIFY, (characteristic, callback))
                )
                return True
        return False

    def stop_notify(self, char_uuid):
        """
        Stop receiving notifications for the specified characteristic UUID.
        """
        if self.connected():
            characteristic = self.get_characteristic_by_uuid(char_uuid)
            if characteristic:
                self.event_queue.put((BLEEvent.BLE_EVENT_STOP_NOTIFY, characteristic))
                return True
        return False

    def write(self, char_uuid, value):
        """
        Write value to the specified characteristic UUID.
        """
        if self.connected():
            characteristic = self.get_characteristic_by_uuid(char_uuid)
            if characteristic:
                self.event_queue.put(
                    (BLEEvent.BLE_EVENT_WRITE, (characteristic, value))
                )
                return True
        return False

    def get_characteristic_by_uuid(self, char_uuid):
        """
        Get the BleakGATTCharacteristic object based on the provided characteristic UUID.
        """
        if self.connected():
            for service in self.services:
                for characteristic in service.characteristics:
                    if characteristic.uuid == char_uuid:
                        return characteristic
        return None

    def __thread_handler(self):
        """
        Entry point for the thread. Runs the event loop and connects to the BLE device.
        """
        asyncio.run(self.__event_handler())

    async def __event_handler(self):
        """
        Connect to the BLE device and handle BLE events.
        """
        try:
            async with BleakClient(self.addr) as self.client:
                if self.pairing:
                    print(f"Start pairing...")
                    paired = await self.client.pair(protection_level=1)
                    print("Pairing: " + ("Success" if paired == True else "Fail"))
                self.conn_status = BLEConnectionStatus.CONNECTED
                self.services = self.client.services
                print("connected")
                while True:
                    # Wait for BLE events
                    if self.event_queue.empty():
                        await asyncio.sleep(0.1)
                        continue
                    (event, data) = self.event_queue.get()

                    # Handle BLE events
                    if event == BLEEvent.BLE_EVENT_DISCONNECT:
                        await self.client.disconnect()
                        self.conn_status = BLEConnectionStatus.DISCONNECTED
                        break
                    elif event == BLEEvent.BLE_EVENT_START_NOTIFY:
                        char_id = data[0]
                        user_callback = data[1]
                        await self.client.start_notify(char_id, user_callback)
                    elif event == BLEEvent.BLE_EVENT_STOP_NOTIFY:
                        char_id = data
                        await self.client.stop_notify(char_id)
                    elif event == BLEEvent.BLE_EVENT_WRITE:
                        char_id = data[0]
                        value = data[1]
                        await self.client.write_gatt_char(char_id, value)
        except Exception as e:
            print(f"Exception: ", e)
            self.conn_timeout = True
