# from core.core_handler import CoreHandler
# from core.core_handler_call_back import CoreHandlerCallBack
# from bleak import BleakClient
# from typing import Callable


# class BioRingHelper(CoreHandlerCallBack):
#     # Init Singleton
#     _instance = None

#     def __new__(cls, *args, **kwargs):
#         if cls._instance is None:
#             cls._instance = super(BioRingHelper, cls).__new__(cls)
#         return cls._instance

#     def __init__(self):
#         self.core_handler = CoreHandler(self)

#     # Command functions - BLE

#     def is_bluetooth_enabled():
#         pass

#     def start_scan(self):
#         self.core_handler.start_scan()

#     def stop_scan():
#         pass

#     def connect():
#         pass

#     def disconnect():
#         pass

#     # Command functions - Device info

#     def get_device_info():
#         pass

#     # Command functions - Data

#     def live_acc_data():
#         pass

#     def live_ecg_data():
#         pass

#     def live_ppg_data():
#         pass

#     def live_temp_data():
#         pass

#     # Listener - BLE

#     def on_device_found():
#         pass

#     def on_device_connected(device: BleakClient):
#         pass

#     def on_device_disconnected():
#         pass

#     # Listener - Device Info

#     def on_device_info_received():
#         pass

#     # Listener - Data

#     def on_acc_data_received():
#         pass

#     def on_ecg_data_received():
#         pass

#     def on_ppg_data_received():
#         pass

#     def on_temp_data_received():
#         pass
