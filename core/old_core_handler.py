import asyncio
from ble.old_ble_manager import OldBleManager
from typing import List, Tuple, Callable
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from core.core_handler_call_back import CoreHandlerCallBack
from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic
from ble.ble_constant import BleConstant
from proto import brp_pb2 as brp
import struct
import logging
import proto.brp_protocol as brp_protocol
from core.handler import TempDataHandler, AccDataHandler, AfeDataHandler
from core.command import (
    GetDeviceInfoCommand,
    LiveAccDataCommand,
    LiveEcgDataCommand,
    LivePpgDataCommand,
    LiveTempDataCommand,
)
from core.handler.streaming.proto.response.res_device_info_handler import ResDeviceInfoHandler


class OldCoreHandler:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(OldCoreHandler, cls).__new__(cls)
        return cls._instance

    def __init__(self, core_handler_call_back: CoreHandlerCallBack):
        self.core_handler_call_back = core_handler_call_back
        self.ble_manager = OldBleManager()
        self.devices: List[Tuple[BLEDevice, AdvertisementData]] = []
        self.proto = brp_protocol.Protocol()

    def start_scan(self) -> List[Tuple[BLEDevice, AdvertisementData]]:
        print("Start scan...")
        # self.devices = asyncio.wait(self.ble_manager.scan())
        self.devices = self.ble_manager.scan()
        print(self.devices)
        return self.devices

    # Support 1 device currently
    def connect(self):
        for device in self.devices:
            self.ble_manager.connect(
                device[0].address, on_device_connected=self._on_device_connected
            )
            print("connecting")

    def disconnect(self):
        self.ble_manager.disconnect()

    # Callback function

    def _on_device_connected(self, client: BleakClient):
        self.core_handler_call_back.on_device_connected(client)
        self.start_notify()

    def start_notify(self):
        self.ble_manager.start_notify(
            BleConstant.BRS_UUID_CHAR_RX, self.brs_rx_char_handler
        )

        self.ble_manager.start_notify(
            BleConstant.BRS_UUID_CHAR_DATA, self.brs_data_char_handler
        )

    def brs_rx_char_handler(self, _sender, data: bytearray):
        rx_pkt = brp.Packet()
        rx_pkt.ParseFromString(bytes(data))
        logging.debug(f"Received packet:\n{rx_pkt}")

        pkt_type = rx_pkt.WhichOneof("payload")
        if pkt_type == "response":
            cid = rx_pkt.response.cid
            if cid in self.rx_rsp_handlers:
                self.rx_rsp_handlers[cid](self, rx_pkt)
        elif pkt_type == "notification":
            nid = rx_pkt.notification.nid
            if nid in self.rx_noti_handlers:
                self.rx_noti_handlers[nid](self, rx_pkt)

    def brs_data_char_handler(self, _sender, data: bytearray):
        # | Type   | Message Index | Length | Value   |
        # |--------|---------------|--------|---------|
        # | 1 byte |    2 byte     | 2 byte | n bytes |
        self.handle_streaming_data(data)

    def data_handler_afe(self, data: bytearray, length: int):
        pass
        # num_samples = int(length / 4)
        # afe_data = struct.unpack(f"<{num_samples}I", data)
        # # logging.debug(f"afe_data: {afe_data}")

        # for i in range(0, num_samples, 1):
        #     fifo_type = afe_data[i] >> 20

        #     if fifo_type == FifoDataType.ECG_AND_FAST_RECOVER_FLAG.value:
        #         ecg_data_one_sample = afe_data[i] & 0x0003FFFF  # Remove the Flag
        #         ecg_data_one_sample = compute.create_a_signed_number(ecg_data_one_sample, 18)

        #         # Write to file ECG ADC value
        #         self.write_record_file(RecordType.ECG, [ecg_data_one_sample])

        #         # Calculate mV value for only display
        #         if self.ecg_mv_unit is True:
        #             # V_ECG(mV) = ADC_VALUE * V_REF_ADC / (2^17 * ECG_GAIN)
        #             ecg_data_one_sample = (ecg_data_one_sample * 1000) / (pow(2, 17) * self.ecg_gain_val)

        #         # logging.debug("ECG data:", ecg_data_one_sample)
        #         ecg_data.append(ecg_data_one_sample)
        #         ecg_idx_data.append(len(ecg_data))
        #     else:
        #         ppg_data = afe_data[i] & 0x000FFFFF  # Remove the Flag

        #         ppg_data = compute.create_a_signed_number(ppg_data, 20)

        #         if fifo_type == FifoDataType.PPG_MEAS_1.value:
        #             red_data.append(ppg_data)
        #             red_idx_data.append(len(red_data))
        #             # logging.debug("AFE measure 1, RED:", ppg_data)
        #             self.ppg_red_data = ppg_data
        #             self.ppg_red_flag = True
        #         elif fifo_type == FifoDataType.PPG_MEAS_2.value:
        #             ir_data.append(ppg_data)
        #             ir_idx_data.append(len(ir_data))
        #             # logging.debug("AFE measure 2, IR:", ppg_data)
        #             self.ppg_ir_data = ppg_data
        #             self.ppg_ir_flag = True
        #         elif fifo_type == FifoDataType.PPG_EXP_OVF.value:
        #             logging.warning("PPG_EXP_OVF_DATA")
        #         else:
        #             # logging.error("AFE format error:", afe_data[i])
        #             return -1

        #         if (self.ppg_red_flag is True) and (self.ppg_ir_flag is True):
        #             self.write_record_file(RecordType.PPG, [self.ppg_red_data, self.ppg_ir_data])
        #             self.ppg_red_flag = False
        #             self.ppg_ir_flag = False

        # return 0

    def data_handler_imu(self, data: bytearray, length: int):
        acc = AccDataHandler.parse(data, length)
        self.core_handler_call_back.on_acc_data_received(acc)

    def data_handler_temperature(self, data: bytearray, _length: int):
        temp_data = TempDataHandler.parse(data)
        self.core_handler_call_back.on_temp_data_received(temp_data)

    def data_handler_log_resp(self, data: bytearray, _length: int):
        pass
        # """Receives log"""
        # log_type_tbl = {0xFF: "DEBUG", 0xFE: "INFO", 0xFD: "WARN"}

        # obj_code_tbl = {
        #     0x00: "BOOTLOADER",
        #     0x01: "APPLICATION",
        #     0x02: "NETWORK"
        # }

        # try:
        #     # Remove the first byte record_type of log
        #     data.pop(0)

        #     i = 0
        #     while i < len(data):
        #         log_type = int.from_bytes(data[i + 0: i + 1], byteorder="little")
        #         obj_code = int.from_bytes(data[i + 1: i + 2], byteorder="little") & 0x7F
        #         timestamp = int.from_bytes(data[i + 2: i + 8], byteorder="little")
        #         data_len = int.from_bytes(data[i + 8: i + 9], byteorder="little")
        #         real_time = timestamp

        #         # 9 bytes of header
        #         i = i + 9
        #         description = data[i: i + data_len].decode("utf-8")

        #         # if self.print_logs:
        #         if log_type < 0xFD:
        #             tool_log = f'\t{real_time} ERR(0x{log_type:02x}) {obj_code_tbl[obj_code]:20} {description}'
        #             logging.error(tool_log)
        #         else:
        #             tool_log = f'\t{real_time} {log_type_tbl[log_type]:9} {obj_code_tbl[obj_code]:20} {description}'
        #             if log_type == 0xFD:
        #                 logging.warning(tool_log)
        #             elif log_type == 0xFE:
        #                 logging.info(tool_log)
        #             else:
        #                 logging.debug(tool_log)

        #         i = i + data_len

        # except Exception as e:
        #     logging.error(f"Exception while parsing log: {e}")

    def data_handle_power(self, data: bytearray, _length: int):
        pass
        # num_samples = 9
        # power_data = struct.unpack(f"<{num_samples}B", data)

        # # RSOC
        # self.uic.lcd_rsoc_display.display(power_data[0])
        # rsoc_data.append(power_data[0])
        # rsoc_idx_data.append(len(rsoc_data))

        # # Voltage (Gauge)
        # voltage_gauge = power_data[1] * 100 + power_data[2]
        # self.uic.lcd_v_bat_fuel_gauge.display(voltage_gauge)

        # # Voltage (Charger)
        # voltage_charger = power_data[3] * 100 + power_data[4]
        # self.uic.lcd_v_bat_charger.display(voltage_charger)

        # # Charging Status
        # self.uic.lbl_charging_status.setText(self.wlc_charging_status_text[power_data[5]])

        # # Poller Connect
        # self.uic.lbl_poller_connect.setText(self.wlc_poller_connect_text[power_data[6]])

        # # Check error
        # if power_data[8] == 0 and power_data[7] == 0:
        #     self.uic.lbl_charging_error.setStyleSheet("color: black")
        #     self.uic.lbl_ntc_status.setStyleSheet("color: black")
        # else:
        #     self.uic.lbl_charging_error.setStyleSheet("color: red")
        #     self.uic.lbl_ntc_status.setStyleSheet("color: red")

        # # Charging Error
        # self.uic.lbl_charging_error.setText(self.wlc_charging_error_text[power_data[7]])

        # # NTC Status
        # self.uic.lbl_ntc_status.setText(self.wlc_ntc_status_text[power_data[8]])

        # return 0

    def data_handle_self_test(self, data: bytearray, _length: int):
        pass
        # num_samples = 1
        # self_test_data = struct.unpack(f"<{num_samples}B", data)

        # # AFE
        # afe_self_test = self_test_data[0] & 0x01
        # self.uic.lbl_self_test_afe.setText(self.self_test_results[afe_self_test])

        # # IMU
        # imu_self_test = (self_test_data[0] >> 1) & 0x01
        # self.uic.lbl_self_test_acc.setText(self.self_test_results[imu_self_test])

        # # Temp
        # temp_self_test = (self_test_data[0] >> 2) & 0x01
        # self.uic.lbl_self_test_temp.setText(self.self_test_results[temp_self_test])

        # # Fuel Gauge
        # gauge_self_test = (self_test_data[0] >> 3) & 0x01
        # self.uic.lbl_self_test_gauge.setText(self.self_test_results[gauge_self_test])

        # # Wireless Charger
        # charger_self_test = (self_test_data[0] >> 4) & 0x01
        # self.uic.lbl_self_test_charger.setText(self.self_test_results[charger_self_test])

    def handle_streaming_data(self, data: bytearray):
        data_handler_map = {
            self.proto.PACKET_TYPE_AFE_DATA: self.data_handler_afe,
            self.proto.PACKET_TYPE_IMU_DATA: self.data_handler_imu,
            self.proto.PACKET_TYPE_TEMPERATURE_DATA: self.data_handler_temperature,
            self.proto.PACKET_TYPE_LOG_DATA: self.data_handler_log_resp,
            self.proto.PACKET_TYPE_POWER_DATA: self.data_handle_power,
            self.proto.PACKET_TYPE_SELF_TEST_DATA: self.data_handle_self_test,
        }

        (data_type, sequence_number, length, value) = self.proto.decode_streaming_data(
            data
        )
        if data_type in data_handler_map:
            data_handler_map[data_type](value, length)

        return 0

    def handle_resp_dev_info(self, pkt: brp.Packet):
        device_info = ResDeviceInfoHandler.parse(pkt)
        self.core_handler_call_back.on_device_info_received(device_info)

    # TODO: Not full implementation
    rx_rsp_handlers = {
        brp.CommandId.CID_DEV_INFO_GET: handle_resp_dev_info,
    }

    def handle_noti_charging_status_changed(self, pkt: brp.Packet):
        self.core_handler_call_back.on_charging_info_received(pkt.notification.charging)
        logging.debug(f"[NT] Charging status: {pkt.notification.charging}")

    def handle_noti_battery_level_changed(self, pkt: brp.Packet):
        self.core_handler_call_back.on_battery_level_received(
            pkt.notification.battery_level
        )
        logging.debug(f"[NT] Battery level: {pkt.notification.battery_level}")

    def handle_noti_hr_spo2(self, pkt: brp.Packet):
        self.core_handler_call_back.on_hr_received(pkt.notification.spo2_hr.hr)
        self.core_handler_call_back.on_spo2_received(pkt.notification.spo2_hr.spo2)
        logging.debug(f"[NT] SPO2: {pkt.notification.spo2_hr.spo2}")
        logging.debug(f"[NT] HR: {pkt.notification.spo2_hr.hr}")
        pass

    rx_noti_handlers = {
        brp.NotificationId.NID_LOG_DATA: None,
        brp.NotificationId.NID_CHARGING_STATUS_CHANGED: handle_noti_charging_status_changed,
        brp.NotificationId.NID_BATTERY_LEVEL_CHANGED: handle_noti_battery_level_changed,
        brp.NotificationId.NID_SPO2_HR_DATA: handle_noti_hr_spo2,
    }

    # Command functions
    def get_device_info(self):
        GetDeviceInfoCommand.send(write_chars=self.ble_manager.write)

    def live_acc_data(self, isStart=True):
        LiveAccDataCommand.send(isStart=isStart, write_chars=self.ble_manager.write)

    def live_ecg_data(self, isStart=True):
        LiveEcgDataCommand.send(isStart=isStart, write_chars=self.ble_manager.write)

    def live_ppg_data(self, isStart=True):
        LivePpgDataCommand.send(isStart=isStart, write_chars=self.ble_manager.write)

    def live_temp_data(self, isStart=True):
        LiveTempDataCommand.send(isStart=isStart, write_chars=self.ble_manager.write)
