import asyncio
import os
from enum import Enum
from typing import List, Optional

from PyQt6.QtWidgets import QApplication, QListWidgetItem
from bleak import BleakClient
from qasync import QEventLoop

from ble.bt_device import BTDevice
from core.enum.ecg_input_polarity import EcgInputPolarity
from core.enum.ecg_sampling_rate import EcgSamplingRate
from core.enum.log_level import LogLevel
from core.enum.power_level import PowerLevel
from core.enum.sensor_type import SensorType
from core.models.device_info import DeviceInfo
from core.models.device_status import DeviceStatus
from core.models.raw_data.accel_data import AccelData
from core.models.raw_data.ecg_data import EcgData
from core.models.raw_data.ppg_data import PpgData
from core.models.raw_data.samples_threshold import SamplesThreshold
from core.models.raw_data.temp_data import TempData
from core.models.self_tests.self_test_result import SelfTestResult
from core.models.settings.accel_settings import AccelSettings
from core.models.settings.bt_settings import BTSettings
from core.models.settings.device_settings import DeviceSettings
from core.models.settings.ecg_settings import EcgSettings, LeadOffSettings
from core.models.settings.log_settings import LogSettings
from core.models.settings.ppg_settings import PpgSettings
from core.utils.time_util import TimeUtil
from errors.common_error import CommonError
from errors.common_result import CommonResult
from gui_wrapper import GuiWrapper
from logger.custom_logger import logger
from managers import ring_factory as factory
from managers.bluetooth_callback import BluetoothCallback
from managers.record_data_callback import RecordDataCallback


class QListItemRole(Enum):
    data = 1


class BioRingTool(BluetoothCallback, RecordDataCallback):
    def __init__(self):
        self.ring_manager = factory.get_ring_manager_instance()
        self.ring_manager.set_bluetooth_callback(self)
        self.ring_manager.set_record_callback(self)
        self.devices: List[BTDevice] = []
        self.selected_scanned_device: Optional[BTDevice] = None
        self.connecting_device: Optional[BTDevice] = None
        self.connected_client: Optional[BleakClient] = None

        app = QApplication([])
        loop = QEventLoop(app)
        asyncio.set_event_loop(loop)

        self.window = GuiWrapper()
        self.window.uic.btn_start_scan.clicked.connect(self.start_scan)
        self.window.uic.btn_stop_scan.clicked.connect(self.stop_scan)
        self.window.uic.scanned_list.itemClicked.connect(self._on_scanned_item_clicked)
        self.window.uic.btn_connect.clicked.connect(self.connect)
        self.window.uic.btn_disconnect.clicked.connect(self.disconnect)
        self.window.uic.btn_get_bluetooth_state.clicked.connect(self.get_bluetooth_state)
        self.window.uic.btn_all_settings.clicked.connect(self.get_all_settings)

        # General
        self.window.uic.btn_get_device_info.clicked.connect(self.get_device_info)
        self.window.uic.btn_get_device_status.clicked.connect(self.get_device_status)

        # Others
        # Self Test
        self.window.uic.btn_enable_bist.clicked.connect(self.enable_bist)
        self.window.uic.btn_disable_bist.clicked.connect(self.disable_bist)
        self.window.uic.btn_get_bist.clicked.connect(self.get_bist)
        self.window.uic.btn_set_bist_interval.clicked.connect(self.set_bist_interval)

        self.window.uic.btn_get_post.clicked.connect(self.get_post)

        # Time syncing
        self.window.uic.btn_set_device_time.clicked.connect(self.set_time_sync)
        self.window.uic.btn_get_device_time.clicked.connect(self.get_time_sync)

        # Power management
        self.window.uic.btn_set_sleep_time.clicked.connect(self.set_sleep_time)
        self.window.uic.btn_factory_reset.clicked.connect(self.factory_reset)
        self.window.uic.btn_reboot.clicked.connect(self.reboot)

        # window = QTGuideWindow(self.close_event)
        # window.scanBtn.clicked.connect(self.start_scan)
        # window.stopBtn.clicked.connect(self.stop_scan)
        # window.connectBtn.clicked.connect(self.connect)

        # window.disconnectBtn.clicked.connect(self.disconnect)
        # window.get_bluetooth_state.clicked.connect(self.get_bluetooth_state)
        # window.set_bluetooth_settings.clicked.connect(self.set_bluetooth_settings)
        #
        # window.get_post.clicked.connect(self.get_post)
        # window.get_bist.clicked.connect(self.get_bist)
        # window.enable_bist.clicked.connect(self.enable_bist)
        # window.disable_bist.clicked.connect(self.disable_bist)
        # window.set_bist_interval.clicked.connect(self.set_bist_interval)
        #
        # window.start_record_ppg.clicked.connect(self.start_record_ppg)
        # window.start_record_ecg.clicked.connect(self.start_record_ecg)
        # window.start_record_acc.clicked.connect(self.start_record_acc)
        # window.start_record_temp.clicked.connect(self.start_record_temp)
        # window.stop_record_ecg.clicked.connect(self.stop_record_ecg)
        # window.stop_record_ppg.clicked.connect(self.stop_record_ppg)
        # window.stop_record_acc.clicked.connect(self.stop_record_acc)
        # window.stop_record_temp.clicked.connect(self.stop_record_temp)
        # window.get_record_sample.clicked.connect(self.get_record_samples_threshold)
        # window.get_record_ppg.clicked.connect(self.get_record_ppg)
        # window.get_record_ecg.clicked.connect(self.get_record_ecg)
        # window.get_record_acc.clicked.connect(self.get_record_acc)
        # window.get_record_temp.clicked.connect(self.get_record_temp)
        #
        # window.get_all_settings.clicked.connect(self.get_all_settings)
        #
        # window.getInfoBtn.clicked.connect(self.get_device_info)
        # window.start_live_acc.clicked.connect(self.start_live_acc_data)
        # window.stop_live_acc.clicked.connect(self.stop_live_acc_data)
        # window.start_live_ecg.clicked.connect(self.start_live_ecg_data)
        # window.stop_live_ecg.clicked.connect(self.stop_live_ecg_data)
        # window.start_live_ppg.clicked.connect(self.start_live_ppg_data)
        # window.stop_live_ppg.clicked.connect(self.stop_live_ppg_data)
        # window.start_live_temp.clicked.connect(self.start_live_temp_data)
        # window.stop_live_temp.clicked.connect(self.stop_live_temp_data)
        #
        # window.set_ppg_settings.clicked.connect(self.set_ppg_settings)
        # window.set_ecg_settings.clicked.connect(self.set_ecg_settings)
        # window.set_acc_settings.clicked.connect(self.set_acc_settings)
        # window.reboot.clicked.connect(self.reboot)
        # window.factory_reset.clicked.connect(self.factory_reset)
        #
        # window.set_time_sync.clicked.connect(self.set_time_sync)
        # window.get_time_sync.clicked.connect(self.get_time_sync)
        # window.set_log_settings.clicked.connect(self.set_log_settings)
        #
        # window.set_sleep_time.clicked.connect(self.set_sleep_time)
        # window.get_device_status.clicked.connect(self.get_device_status)
        # window.get_protocol_info.clicked.connect(self.get_protocol_info)
        # window.update_firmware.clicked.connect(self.update_firmware)

        # # Create the Bluetooth state receiver
        # self.bt_receiver = BluetoothStateReceiver()
        # self.bt_receiver.bluetoothStateChanged.connect(self.handle_bluetooth_state_change)
        #
        # # Start the Bluetooth listener thread
        # self.bt_listener_thread = BluetoothListenerThread(self.bt_receiver.bluetoothStateChanged.emit)
        # self.bt_listener_thread.start()

        self.window.show()
        # Run the PyQt event loop alongside asyncio
        with loop:
            loop.run_forever()

    def close_event(self):
        # Stop the Bluetooth listener thread when closing the application
        logger.info('close event')
        # self.bt_listener_thread.stop()
        # self.bt_listener_thread.join()

    def handle_bluetooth_state_change(self, state: str):
        logger.info(f"Bluetooth state changed: {state}")

    def _on_scanned_item_clicked(self, item: QListWidgetItem):
        self.selected_scanned_device = item.data(QListItemRole.data.value)

    def set_bluetooth_settings(self):
        self.ring_manager.set_bluetooth_settings(
            self.devices[0].address,
            BTSettings(
                adv_name="BioRing Hieu3",
                adv_interval=318.5,
                connection_interval_min=20.12,
                connection_interval_max=20.9123456789,
                slave_latency=3,
                transmit_power_level=PowerLevel.POS_4,
            ),
            self.on_bluetooth_settings_set,
        )

    def on_bluetooth_settings_set(self, result: CommonResult):
        logger.info(f"on_bluetooth_settings_set Result: {result}")

    """ BLE actions"""

    def start_scan(self):
        self.ring_manager.start_scan()

    def stop_scan(self):
        self.ring_manager.stop_scan()

    def connect(self):
        if self.selected_scanned_device is not None:
            self.ring_manager.connect(self.selected_scanned_device.address, 10)
            self.connecting_device = self.selected_scanned_device
            logger.info(f'connect to device: ${self.selected_scanned_device}')
            return

        logger.info("No device selected")

    def disconnect(self):
        self.ring_manager.disconnect(self.connected_client.address)

    def get_bluetooth_state(self):
        state = self.ring_manager.get_bluetooth_state()
        logger.info(state)
        self.window.uic.bluetooth_state.setText("ON" if state else "OFF")

    """ BluetoothCallback """

    def on_scan_result(self, device: BTDevice):
        logger.info(f"on_scan_result Device found: {device}")
        self.devices.append(device)

        item = QListWidgetItem()
        item.setData(QListItemRole.data.value, device)
        item.setText(f"{device.name} - {device.address}")

        self.window.uic.scanned_list.addItem(item)

    def on_device_connected(self, device: BleakClient):
        logger.info(f"on_device_connected Device connected: {device}")
        self.connected_client = device
        self.window.uic.connected_device_dropdown.addItem(f"{self.connecting_device.name} - {device.address}", device)

    def on_bluetooth_error(self, device: BTDevice, error: CommonError):
        logger.info(f"on_bluetooth_error Error: {error}")

    def on_bluetooth_state_changed(self, status: bool):
        pass

    # Self test
    def get_post(self):
        self.ring_manager.get_post(self.connected_client.address, self.on_post_result)

    def on_post_result(self, result: CommonResult, post: Optional[SelfTestResult]):
        if result.is_success:
            self.window.uic.self_test_post_afe_enabled.setChecked(post.afe)
            self.window.uic.self_test_post_accel_enabled.setChecked(post.accel)
            self.window.uic.self_test_post_temp_enabled.setChecked(post.temp)
            self.window.uic.self_test_post_wg_enabled.setChecked(post.wireless_charger)
            self.window.uic.self_test_post_fuel_gauge_enabled.setChecked(post.fuel_gauge)
            return

        logger.info(f"Result: {result}")

    def get_bist(self):
        self.ring_manager.get_bist(self.connected_client.address, self.on_bist_result)

    def on_bist_result(self, result: CommonResult, bist: Optional[SelfTestResult]):
        if result.is_success:
            self.window.uic.self_test_bist_afe_enabled.setChecked(bist.afe)
            self.window.uic.self_test_bist_accel_enabled.setChecked(bist.accel)
            self.window.uic.self_test_bist_temp_enabled.setChecked(bist.temp)
            self.window.uic.self_test_bist_wg_enabled.setChecked(bist.wireless_charger)
            self.window.uic.self_test_bist_fuel_gauge_enabled.setChecked(bist.fuel_gauge)
            return

        logger.info(f"Result: {result}")

    def enable_bist(self):
        self.ring_manager.enable_bist(self.connected_client.address, self.on_enable_bist_result)

    def on_enable_bist_result(self, result: CommonResult):
        logger.info(f"on_enable_bist_result Result: {result}")

    def disable_bist(self):
        self.ring_manager.disable_bist(self.connected_client.address, self.on_disable_bist_result)

    def on_disable_bist_result(self, result: CommonResult):
        logger.info(f"on_disable_bist_result Result: {result}")

    def set_bist_interval(self):
        try:
            interval = int(self.window.uic.input_bist_interval.text())
            self.ring_manager.set_bist_interval(
                self.connected_client.address,
                interval,
                self.on_set_bist_interval_result
            )

        except ValueError:
            logger.error("Invalid BIST interval input")

    def on_set_bist_interval_result(self, result: CommonResult):
        logger.info(f"on_set_bist_interval_result Result: {result}")

    # Command functions - Device info

    def get_device_info(self):
        self.ring_manager.get_device_info(self.connected_client.address, self.on_device_info)

    def on_device_info(self, result: CommonResult, info: Optional[DeviceInfo]):
        if result.is_success:
            self.window.uic.info_serial_number.setText(info.serial_number)
            self.window.uic.info_manufacturing_date.setText(info.manufacturing_date)
            self.window.uic.info_lot.setText(info.lot)
            self.window.uic.info_model.setText(info.model)
            self.window.uic.info_pcba_version.setText(info.pcba_version)
            self.window.uic.info_bootloader_version.setText(info.bootloader_version)
            self.window.uic.info_aplication_version.setText(info.application_version)
            self.window.uic.info_build_date.setText(info.build_date)
            return

        logger.info(f"on_device_info Result: {result}")

    # Command functions - Data

    def start_live_acc_data(self):
        self.ring_manager.start_streaming_accel_data(self.devices[0].address, self.on_acc_data_received)

    def on_acc_data_received(self, result: CommonResult, data: Optional[AccelData], packet_lost: int):
        logger.info(f"on_acc_data_received Result: {result}")
        logger.info(f"on_acc_data_received Data: {data}")

    def stop_live_acc_data(self):
        self.ring_manager.stop_streaming_data(self.devices[0].address, SensorType.ACCEL, self.on_stop_acc_success)

    def on_stop_acc_success(self, result: CommonResult):
        logger.info(f"on_stop_acc_success Result: {result}")

    def start_live_ecg_data(self):
        self.ring_manager.start_streaming_ecg_data(self.devices[0].address, self.on_ecg_data_received)

    def on_ecg_data_received(self, result: CommonResult, data: Optional[EcgData], packet_lost: int):
        logger.info(f"on_ecg_data_received Result: {result}")
        logger.info(f"on_ecg_data_received Data: {data}")

    def stop_live_ecg_data(self):
        self.ring_manager.stop_streaming_data(self.devices[0].address, SensorType.ECG, self.on_stop_ecg_success)

    def on_stop_ecg_success(self, result: CommonResult):
        logger.info(f"on_stop_ecg_success Result: {result}")

    def start_live_ppg_data(self):
        self.ring_manager.start_streaming_ppg_data(self.devices[0].address, self.on_ppg_data_received)

    def on_ppg_data_received(self, result: CommonResult, data: Optional[PpgData], packet_lost: int):
        logger.info(f"on_ppg_data_received Result: {result}")
        logger.info(f"on_ppg_data_received Data: {data}")

    def stop_live_ppg_data(self):
        self.ring_manager.stop_streaming_data(self.devices[0].address, SensorType.PPG, self.on_stop_ppg_success)

    def on_stop_ppg_success(self, result: CommonResult):
        logger.info(f"on_stop_ppg_success Result: {result}")

    def start_live_temp_data(self):
        self.ring_manager.start_streaming_temp_data(self.devices[0].address, self.on_temp_data_received)

    def on_temp_data_received(self, result: CommonResult, data: Optional[TempData], packet_lost: int):
        logger.info(f"on_temp_data_received Result: {result}")
        logger.info(f"on_temp_data_received Data: {data}")

    def stop_live_temp_data(self):
        self.ring_manager.stop_streaming_data(self.devices[0].address, SensorType.TEMP, self.on_stop_temp_success)

    def on_stop_temp_success(self, result: CommonResult):
        logger.info(f"on_stop_temp_success Result: {result}")

    # Listener - BLE

    def on_device_found(self):
        pass

    # def on_device_connected(self, device: BleakClient):
    #     # self.core_handler.start_notify()
    #     pass

    def on_device_disconnected(self):
        pass

    # Listener - Device Info

    def on_device_info_received(self, device: DeviceInfo):
        logger.info(device)

    def on_charging_info_received(self, charging: bool):
        logger.info(f"[NT] Charging status: {charging}")

    def on_battery_level_received(self, battery_level: int):
        logger.info(f"[NT] Battery level: {battery_level}")

    def on_hr_received(self, hr: int):
        logger.info(f"[NT] HR: {hr}")

    def on_spo2_received(self, spo2: int):
        logger.info(f"[NT] SpO2: {spo2}")

    # Listener - Data

    def on_record_finished(self, device: BTDevice, sensor_type: SensorType):
        logger.info(f"[NT] Record finished: {sensor_type}, device: {device}")

    def on_accel_recorded(self, device: BTDevice, data: AccelData):
        logger.info(f'device: {device}, data: {data}')

    def on_ecg_recorded(self, device: BTDevice, data: EcgData):
        logger.info(f'device: {device}, data: {data}')

    def on_ppg_recorded(self, device: BTDevice, data: PpgData):
        logger.info(f'device: {device}, data: {data}')

    def on_temp_recorded(self, device: BTDevice, data: TempData):
        logger.info(f'device: {device}, data: {data}')

    def on_record_error(self, device: BTDevice, data: CommonError):
        logger.info(f'device: {device}, data: {data}')

    def start_record_ppg(self):
        self.ring_manager.start_record(self.devices[0].address, 3000, SensorType.PPG, self.on_start_record_ppg_success)

    def start_record_ecg(self):
        self.ring_manager.start_record(self.devices[0].address, 3000, SensorType.ECG, self.on_start_record_ecg_success)

    def start_record_acc(self):
        self.ring_manager.start_record(self.devices[0].address, 100, SensorType.ACCEL, self.on_start_record_acc_success)

    def start_record_temp(self):
        self.ring_manager.start_record(self.devices[0].address, 3000, SensorType.TEMP,
                                       self.on_start_record_temp_success)

    def on_start_record_ppg_success(self, result: CommonResult):
        logger.info(f"on_record_ppf_success Result: {result}")

    def on_start_record_ecg_success(self, result: CommonResult):
        logger.info(f"on_record_ecg_success Result: {result}")

    def on_start_record_acc_success(self, result: CommonResult):
        logger.info(f"on_record_acc_success Result: {result}")

    def on_start_record_temp_success(self, result: CommonResult):
        logger.info(f"on_record_temp_success Result: {result}")

    def stop_record_ecg(self):
        self.ring_manager.stop_record(self.devices[0].address, SensorType.ECG, self.on_stop_record_ecg_success)

    def on_stop_record_ecg_success(self, result: CommonResult):
        logger.info(f"on_stop_record_ecg_success Result: {result}")

    def stop_record_ppg(self):
        self.ring_manager.stop_record(self.devices[0].address, SensorType.PPG, self.on_stop_record_ppg_success)

    def on_stop_record_ppg_success(self, result: CommonResult):
        logger.info(f"on_stop_record_ppg_success Result: {result}")

    def stop_record_acc(self):
        self.ring_manager.stop_record(self.devices[0].address, SensorType.ACCEL, self.on_stop_record_acc_success)

    def on_stop_record_acc_success(self, result: CommonResult):
        logger.info(f"on_stop_record_acc_success Result: {result}")

    def stop_record_temp(self):
        self.ring_manager.stop_record(self.devices[0].address, SensorType.TEMP, self.on_stop_record_temp_success)

    def on_stop_record_temp_success(self, result: CommonResult):
        logger.info(f"on_stop_record_temp_success Result: {result}")

    def get_record_ppg(self):
        self.ring_manager.get_record(self.devices[0].address, SensorType.PPG, 0)

    def get_record_ecg(self):
        self.ring_manager.get_record(self.devices[0].address, SensorType.ECG, 0)

    def get_record_acc(self):
        self.ring_manager.get_record(self.devices[0].address, SensorType.ACCEL, 0)

    def get_record_temp(self):
        self.ring_manager.get_record(self.devices[0].address, SensorType.TEMP, 0)

    def on_get_record_success(self, result: CommonResult):
        logger.info(f"on_get_record_success Result: {result}")

    def get_record_samples_threshold(self):
        self.ring_manager.get_record_samples_threshold(self.devices[0].address, self.on_get_record_samples_threshold)

    def on_get_record_samples_threshold(self, result: CommonResult, samples_threshold: Optional[SamplesThreshold]):
        logger.info(f"on_get_record_samples_threshold Result: {result}")
        logger.info(f"on_get_record_samples_threshold Samples threshold: {samples_threshold}")

    def get_all_settings(self):
        self.ring_manager.get_all_settings(self.devices[0].address, self.on_all_settings_received)

    def on_all_settings_received(self, result: CommonResult, settings: Optional[DeviceSettings]):
        logger.info(f"on_all_settings_received Result: {result}")
        logger.info(f"on_all_settings_received Settings: {settings}")

    def set_ppg_settings(self):
        self.ring_manager.set_ppg_settings(
            self.devices[0].address, PpgSettings(
                enable=False,
                # enable_ir_led=False,
                # enable_red_led=True,
                # red_led_current=10,
                # ir_led_current=10,
                # sampling_rate=PpgSamplingRate.PPG_SAMPLE_RATE_128HZ,
            ),
            self.on_ppg_settings_set
        )

    def on_ppg_settings_set(self, result: CommonResult):
        logger.info(f"on_ppg_settings_set Result: {result}")

    def set_ecg_settings(self):
        self.ring_manager.set_ecg_settings(
            self.devices[0].address,
            EcgSettings(
                enable=True,
                sampling_rate=EcgSamplingRate.ECG_SAMPLE_RATE_128HZ,
                # ina_gain= EcgInaGain.INA_GAIN_0,
                # ina_range= EcgInaRange.ECG_INA_GAIN_RGE_0,
                # pga_gain= EcgPgaGain.PGA_GAIN_16,
                input_polarity=EcgInputPolarity.ECG_INPUT_NON_INVERTED,
                lead_off_enable=False,
                lead_off_settings=LeadOffSettings(

                    # mode= EcgLeadOffMode.ECG_LEAD_OFF_DC,
                    # current_polarity= EcgLeadOffCurrentPolarity.ECG_LEAD_OFF_NON_INVERTED,
                    # current_magnitude=EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_0,
                    # voltage_threshold=EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_25MV,
                    # lead_off_frequency=EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_DISABLE,
                )
            ),
            self.on_ecg_settings_set
        )

    def on_ecg_settings_set(self, result: CommonResult):
        logger.info(f"on_ppg_settings_set Result: {result}")

    def set_acc_settings(self):
        self.ring_manager.set_accel_settings(
            self.devices[0].address,
            AccelSettings(
                enable=False,
            ),
            self.on_acc_settings_set,
        )

    def on_acc_settings_set(self, result: CommonResult):
        logger.info(f"on_acc_settings_set Result: {result}")

    def reboot(self):
        self.ring_manager.reboot(self.connected_client.address, self.on_reboot_success)

    def on_reboot_success(self, result: CommonResult):
        logger.info(f"on_reboot_success Result: {result}")

    def factory_reset(self):
        self.ring_manager.factory_reset(self.connected_client.address, self.on_factory_reset_success)

    def on_factory_reset_success(self, result: CommonResult):
        logger.info(f"on_factory_reset_success Result: {result}")

    def set_time_sync(self):
        try:
            time = int(self.window.uic.input_time_syncing_device_time.text())
            self.ring_manager.set_time_sync(
                self.connected_client.address,
                time,
                self.on_time_sync_success
            )

        except ValueError:
            logger.error("Invalid Time (epoch) input")

    def on_time_sync_success(self, result: CommonResult):
        logger.info(f"on_time_sync_success Result: {result}")

    def get_time_sync(self):
        self.ring_manager.get_time_sync(self.connected_client.address, self.on_time_sync_get_success)

    def on_time_sync_get_success(self, result: CommonResult, time: int):
        device_time = TimeUtil.from_epoch_to_ymdhms(time)
        self.window.uic.time_syncing_device_time.setText(device_time)

    def set_log_settings(self):
        self.ring_manager.set_log_settings(
            self.devices[0].address, LogSettings(
                enable=True,
                levels=[
                    LogLevel.INFO,
                    LogLevel.ERROR,
                    LogLevel.WARNING,
                    LogLevel.DEBUG
                ]
            ), self.on_log_settings_success)

    def on_log_settings_success(self, result: CommonResult):
        logger.info(f"on_log_settings_success Result: {result}")

    def set_sleep_time(self):
        try:
            time = int(self.window.uic.input_power_management_sleep_time.text())
            self.ring_manager.set_sleep_time(
                self.connected_client.address,
                time,
                self.on_sleep_time_success
            )

        except ValueError:
            logger.error("Invalid Time (in seconds) input")

    def on_sleep_time_success(self, result: CommonResult):
        logger.info(f"on_sleep_time_success Result: {result}")

    def get_device_status(self):
        self.ring_manager.get_device_status(self.connected_client.address, self.on_device_status_success)

    def on_device_status_success(self, result: CommonResult, device_status: Optional[DeviceStatus]):
        if result.is_success:
            self.window.uic.status_current_app.setText(device_status.current_app.name)

            device_time = TimeUtil.from_epoch_to_ymdhms(device_status.device_time)
            self.window.uic.status_device_time.setText(device_time)

            post_time = TimeUtil.from_epoch_to_ymdhms(device_status.post_timestamp)
            self.window.uic.status_post_timestamp.setText(post_time)

            bist_time = TimeUtil.from_epoch_to_ymdhms(device_status.bist_timestamp)
            self.window.uic.status_bist_timestamp.setText(bist_time)

            self.window.uic.status_battery_level.display(device_status.battery_level)
            self.window.uic.status_charging_error.setText(str(device_status.charging_error.name))
            self.window.uic.status_charging_status.setText(str(device_status.is_charging.name))

            # POST result
            self.window.uic.status_post_afe_enabled.setChecked(device_status.post_result.afe)
            self.window.uic.status_post_accel_enabled.setChecked(device_status.post_result.accel)
            self.window.uic.status_post_temp_enabled.setChecked(device_status.post_result.temp)
            self.window.uic.status_post_wireless_charger_enabled.setChecked(device_status.post_result.wireless_charger)
            self.window.uic.status_post_fuel_gauge_enabled.setChecked(device_status.post_result.fuel_gauge)

            # BIST result
            self.window.uic.status_bist_afe_enabled.setChecked(device_status.bist_result.afe)
            self.window.uic.status_bist_accel_enabled.setChecked(device_status.bist_result.accel)
            self.window.uic.status_bist_temp_enabled.setChecked(device_status.bist_result.temp)
            self.window.uic.status_bist_wireless_charger_enabled.setChecked(device_status.bist_result.wireless_charger)
            self.window.uic.status_bist_fuel_gauge_enabled.setChecked(device_status.bist_result.fuel_gauge)
            return

        logger.info(f"on_device_status_success Result: {result}")
        logger.info(f"on_device_status_success Device status: {device_status}")

    def get_protocol_info(self):
        self.ring_manager.get_protocol_info(self.devices[0].address, self.on_protocol_info_success)

    def on_protocol_info_success(self, result: CommonResult, protocol_info: Optional[str]):
        logger.info(f"on_protocol_info_success Result: {result}")
        logger.info(f"on_protocol_info_success Protocol info: {protocol_info}")


    def update_firmware(self):
        # Get the current file's path
        current_file = os.path.abspath(__file__)

        # Get the directory of the current file
        current_dir = os.path.dirname(current_file)

        # Build the path to the file inside the project folder
        file_path = os.path.join(current_dir, 'data', 'bioring_app1_hw0.2_v0.4.1.0.cyacd2')

        self.ring_manager.update_firmware(self.devices[0].address, file_path, self.on_firmware_update_success)

    def on_firmware_update_success(self, result: CommonResult):
        logger.info(f"on_firmware_update_success Result: {result}")
