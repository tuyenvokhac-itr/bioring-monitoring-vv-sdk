import asyncio
from enum import Enum
from threading import Thread, Event
from bleak import BleakScanner
from bleak import BleakClient
from .ble_constant import BleConstant
import platform
from typing import Callable

OnDeviceConnected = Callable[[BleakClient], None]


class BLEConnectionStatus(Enum):
    INIT = 0
    CONNECTING = 1
    CONNECTED = 2
    DISCONNECTED = 3


class BleManager:
    def __init__(self, debug=False):
        self.debug = debug
        self.device_addr = ""
        self.conn_status = BLEConnectionStatus.INIT
        self.conn_timeout = False

        if platform.system() == "Darwin":  # macOS
            self.use_bdaddr = False
        elif platform.system() == "Windows":  # Windows
            self.use_bdaddr = True
        else:
            self.use_bdaddr = False

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
            print(d)
            if d.name != None and BleConstant.BIORING_PREFIX in d.name:
                self.filtered_devices.append((d, a))
        return self.filtered_devices

    def scan_dfu(self):
        """
        Scan for nearby DFU BLE devices.
        """
        devices = asyncio.run(BleakScanner.discover())
        self.filtered_devices = []
        for d in devices:
            if d.name != None and BleConstant.BIORING_DFU_PREFIX in d.name:
                self.filtered_devices.append(d)
        return self.filtered_devices

    def connect(self, addr, pairing=False, onDeviceConnected: OnDeviceConnected = None):
        """
        Start the thread for establishing and managing the BLE connection.
        """
        self.addr = addr
        self.pairing = pairing
        self.conn_timeout = False
        self.thread = Thread(target=self.__thread_handler, args=(onDeviceConnected,))
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
        # self.event_queue.put((BLEEvent.BLE_EVENT_DISCONNECT, None))
        if self.connected():
            if self.thread.is_alive():
                self.thread.join()

    def connected(self):
        return self.conn_status == BLEConnectionStatus.CONNECTED

    def __thread_handler(self, onDeviceConnected: OnDeviceConnected = None):
        """
        Entry point for the thread. Runs the event loop and connects to the BLE device.
        """
        asyncio.run(self.__event_handler(onDeviceConnected=onDeviceConnected))

    async def __event_handler(self, onDeviceConnected: OnDeviceConnected = None):
        """
        Connect to the BLE device and handle BLE events.
        """
        try:
            async with BleakClient(self.addr) as self.client:
                print("connected")
                onDeviceConnected(self.client)
                # if self.pairing:
                #     print(f"Start pairing...")
                #     paired = await self.client.pair(protection_level=1)
                #     print("Pairing: " + ("Success" if paired == True else "Fail"))
                # self.conn_status = BLEConnectionStatus.CONNECTED
                # self.services = self.client.services
                # print("connected")
                # while True:
                #     # Wait for BLE events
                #     if self.event_queue.empty():
                #         await asyncio.sleep(0.1)
                #         continue
                #     (event, data) = self.event_queue.get()

                #     # Handle BLE events
                #     if event == BLEEvent.BLE_EVENT_DISCONNECT:
                #         await self.client.disconnect()
                #         self.conn_status = BLEConnectionStatus.DISCONNECTED
                #         break
                #     elif event == BLEEvent.BLE_EVENT_START_NOTIFY:
                #         char_id = data[0]
                #         user_callback = data[1]
                #         await self.client.start_notify(char_id, user_callback)
                #     elif event == BLEEvent.BLE_EVENT_STOP_NOTIFY:
                #         char_id = data
                #         await self.client.stop_notify(char_id)
                #     elif event == BLEEvent.BLE_EVENT_WRITE:
                #         char_id = data[0]
                #         value = data[1]
                #         await self.client.write_gatt_char(char_id, value)
        except Exception as e:
            print(f"Exception: ", e)
            self.conn_timeout = True
