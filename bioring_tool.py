import asyncio
import os
from enum import Enum
from typing import List, Optional

from PyQt6.QtWidgets import QApplication, QListWidgetItem
from bleak import BleakClient
from qasync import QEventLoop

from ble.bt_device import BTDevice
from core.enum.accel_full_scale_range import AccelFullScaleRange
from core.enum.accel_sampling_rate import AccelSamplingRate
from core.enum.ecg_ina_gain import EcgInaGain
from core.enum.ecg_ina_range import EcgInaRange
from core.enum.ecg_input_polarity import EcgInputPolarity
from core.enum.ecg_lead_off_current_magnitude import EcgLeadOffCurrentMagnitude
from core.enum.ecg_lead_off_current_polarity import EcgLeadOffCurrentPolarity
from core.enum.ecg_lead_off_freq import EcgLeadOffFreq
from core.enum.ecg_lead_off_mode import EcgLeadOffMode
from core.enum.ecg_lead_off_voltage_threshold import EcgLeadOffVoltageThreshold
from core.enum.ecg_pga_gain import EcgPgaGain
from core.enum.ecg_sampling_rate import EcgSamplingRate
from core.enum.log_level import LogLevel
from core.enum.power_level import PowerLevel
from core.enum.ppg_sampling_rate import PpgSamplingRate
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
        self.set_up_click_listener()
        self.init_static_data()
        self.window.show()

        with loop:
            loop.run_forever()

    def set_up_click_listener(self):
        # BLE connection
        self.window.uic.btn_start_scan.clicked.connect(self.start_scan)
        self.window.uic.btn_stop_scan.clicked.connect(self.stop_scan)
        self.window.uic.scanned_list.itemClicked.connect(self.on_scanned_item_clicked)
        self.window.uic.btn_connect.clicked.connect(self.connect)

        self.window.uic.btn_disconnect.clicked.connect(self.disconnect)
        self.window.uic.btn_get_bluetooth_state.clicked.connect(self.get_bluetooth_state)

        # Device info
        self.window.uic.btn_get_device_info.clicked.connect(self.get_device_info)
        self.window.uic.btn_get_device_status.clicked.connect(self.get_device_status)

        # Self test
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

        # Data recording
        self.window.uic.btn_get_thresholds.clicked.connect(self.get_record_samples_threshold)
        self.window.uic.btn_start_record.clicked.connect(self.start_record)
        self.window.uic.btn_stop_record.clicked.connect(self.stop_record)
        self.window.uic.btn_get_record.clicked.connect(self.get_record)

        # Settings
        # ECG settings
        self.window.uic.btn_save_ecg_settings.clicked.connect(self.set_ecg_settings)

        # ACCEL settings
        self.window.uic.btn_save_accel_settings.clicked.connect(self.set_acc_settings)

        # PPG settings
        self.window.uic.btn_save_ppg_settings.clicked.connect(self.set_ppg_settings)

        # Log settings
        self.window.uic.btn_save_log_level.clicked.connect(self.set_log_settings)

        # BLE settings
        self.window.uic.btn_save_ble_settings.clicked.connect(self.set_bluetooth_settings)

        # Get all settings
        self.window.uic.btn_get_all_settings.clicked.connect(self.get_all_settings)

    def init_static_data(self):
        # Data recording
        for sensor in SensorType:
            self.window.uic.start_record_sensor_type.addItem(sensor.name, sensor)
            self.window.uic.stop_record_sensor_type.addItem(sensor.name, sensor)
            self.window.uic.get_record_sensor_type.addItem(sensor.name, sensor)

        # ECG settings
        for rate in EcgSamplingRate:
            self.window.uic.box_ecg_settings_sampling_rate.addItem(rate.name, rate)

        for gain in EcgPgaGain:
            self.window.uic.box_ecg_settings_pga_gain.addItem(gain.name, gain)

        for ina_gain in EcgInaGain:
            self.window.uic.box_ecg_settings_ina_gain.addItem(ina_gain.name, ina_gain)

        for ina_range in EcgInaRange:
            self.window.uic.box_ecg_settings_ina_range.addItem(ina_range.name, ina_range)

        for polarity in EcgInputPolarity:
            self.window.uic.box_ecg_settings_input_polarity.addItem(polarity.name, polarity)

        for lead_off_mode in EcgLeadOffMode:
            self.window.uic.box_lead_off_settings_mode.addItem(lead_off_mode.name, lead_off_mode)

        for current_polarity in EcgLeadOffCurrentPolarity:
            self.window.uic.box_lead_off_settings_current_polarity.addItem(current_polarity.name, current_polarity)

        for current_magnitude in EcgLeadOffCurrentMagnitude:
            self.window.uic.box_lead_off_settings_current_magnitude.addItem(current_magnitude.name, current_magnitude)

        for voltage_threshold in EcgLeadOffVoltageThreshold:
            self.window.uic.box_lead_off_settings_current_threshold.addItem(voltage_threshold.name, voltage_threshold)

        for lead_off_freq in EcgLeadOffFreq:
            self.window.uic.box_lead_off_settings_frequency.addItem(lead_off_freq.name, lead_off_freq)

        # ACCEL settings
        for rate in AccelSamplingRate:
            self.window.uic.box_accel_settings_sampling_rate.addItem(rate.name, rate)

        for full_scale_range in AccelFullScaleRange:
            self.window.uic.box_accel_settings_full_scale_range.addItem(full_scale_range.name, full_scale_range)

        # PPG settings
        for rate in PpgSamplingRate:
            self.window.uic.box_ppg_settings_sampling_rate.addItem(rate.name, rate)

        # BLE settings
        for power_level in PowerLevel:
            self.window.uic.box_ble_settings_tx_power_level.addItem(power_level.name, power_level)

    def close_event(self):
        # Stop the Bluetooth listener thread when closing the application
        logger.info('close event')
        # self.bt_listener_thread.stop()
        # self.bt_listener_thread.join()

    """ ******************************** BLE actions ******************************** """

    def start_scan(self):
        self.ring_manager.start_scan()

    def stop_scan(self):
        self.ring_manager.stop_scan()

    def on_scanned_item_clicked(self, item: QListWidgetItem):
        self.selected_scanned_device = item.data(QListItemRole.data.value)

    def connect(self):
        if self.selected_scanned_device is not None:
            self.ring_manager.connect(self.selected_scanned_device.address, 10)
            self.connecting_device = self.selected_scanned_device
            logger.info(f'Connect to device: ${self.selected_scanned_device}')
            return

        logger.error("No device selected")

    def disconnect(self):
        self.ring_manager.disconnect(self.connected_client.address)

    def get_bluetooth_state(self):
        state = self.ring_manager.get_bluetooth_state()
        self.window.uic.bluetooth_state.setText("ON" if state else "OFF")

    """ BluetoothCallback """

    def on_scan_result(self, device: BTDevice):
        self.devices.append(device)

        item = QListWidgetItem()
        item.setData(QListItemRole.data.value, device)
        item.setText(f"{device.name} - {device.address}")

        self.window.uic.scanned_list.addItem(item)

    def on_device_connected(self, device: BleakClient):
        self.connected_client = device
        self.window.uic.connected_device_dropdown.addItem(f"{self.connecting_device.name} - {device.address}", device)

    def on_bluetooth_error(self, device: BTDevice, error: CommonError):
        logger.info(f"Error: {error}")

    def on_bluetooth_state_changed(self, status: bool):
        pass

    """ ******************************* Settings ******************************* """

    # ECG settings
    def set_ecg_settings(self):
        ecg_enabled = self.window.uic.ecg_settings_enabled.isChecked()
        sampling_rate = self.window.uic.box_ecg_settings_sampling_rate.currentData()
        pga_gain = self.window.uic.box_ecg_settings_pga_gain.currentData()
        ina_gain = self.window.uic.box_ecg_settings_ina_gain.currentData()
        ina_range = self.window.uic.box_ecg_settings_ina_range.currentData()
        input_polarity = self.window.uic.box_ecg_settings_input_polarity.currentData()

        lead_off_enabled = self.window.uic.lead_off_settings_enabled.isChecked()
        lead_off_mode = self.window.uic.box_lead_off_settings_mode.currentData()
        lead_off_current_polarity = self.window.uic.box_lead_off_settings_current_polarity.currentData()
        lead_off_current_magnitude = self.window.uic.box_lead_off_settings_current_magnitude.currentData()
        lead_off_voltage_threshold = self.window.uic.box_lead_off_settings_current_threshold.currentData()
        lead_off_frequency = self.window.uic.box_lead_off_settings_frequency.currentData()

        self.ring_manager.set_ecg_settings(
            self.connected_client.address,
            EcgSettings(
                enable=ecg_enabled,
                sampling_rate=sampling_rate,
                pga_gain=pga_gain,
                ina_gain=ina_gain,
                ina_range=ina_range,
                input_polarity=input_polarity,
                lead_off_enable=lead_off_enabled,
                lead_off_settings=LeadOffSettings(
                    mode=lead_off_mode,
                    current_polarity=lead_off_current_polarity,
                    current_magnitude=lead_off_current_magnitude,
                    voltage_threshold=lead_off_voltage_threshold,
                    lead_off_frequency=lead_off_frequency,
                )
            ),
            self.on_ecg_settings_set
        )

    def on_ecg_settings_set(self, result: CommonResult):
        logger.info(f"Result: {result}")

    # ACCEL settings
    def set_acc_settings(self):
        accel_enabled = self.window.uic.accel_settings_enabled.isChecked()
        sampling_rate = self.window.uic.box_accel_settings_sampling_rate.currentData()
        full_scale_range = self.window.uic.box_accel_settings_full_scale_range.currentData()

        self.ring_manager.set_accel_settings(
            self.devices[0].address,
            AccelSettings(
                enable=accel_enabled,
                sampling_rate=sampling_rate,
                full_scale_range=full_scale_range,
            ),
            self.on_acc_settings_set,
        )

    def on_acc_settings_set(self, result: CommonResult):
        logger.info(f"Result: {result}")

    # PPG settings
    def set_ppg_settings(self):
        ppg_enabled = self.window.uic.ppg_settings_enabled.isChecked()
        red_led_enabled = self.window.uic.ppg_settings_red_led_enabled.isChecked()
        ir_led_enabled = self.window.uic.ppg_settings_ir_led_enabled.isChecked()
        red_led_current = float(self.window.uic.input_red_led_current.text())
        ir_led_current = float(self.window.uic.input_ir_led_current.text())
        sampling_rate = self.window.uic.box_ppg_settings_sampling_rate.currentData()

        self.ring_manager.set_ppg_settings(
            self.devices[0].address, PpgSettings(
                enable=ppg_enabled,
                enable_ir_led=ir_led_enabled,
                enable_red_led=red_led_enabled,
                red_led_current=red_led_current,
                ir_led_current=ir_led_current,
                sampling_rate=sampling_rate,
            ),
            self.on_ppg_settings_set
        )

    def on_ppg_settings_set(self, result: CommonResult):
        logger.info(f"Result: {result}")

    # Log settings
    def set_log_settings(self):
        log_error = self.window.uic.cbox_log_settings_error.isChecked()
        log_warning = self.window.uic.cbox_log_settings_warning.isChecked()
        log_info = self.window.uic.cbox_log_settings_info.isChecked()
        log_debug = self.window.uic.cbox_log_settings_debug.isChecked()
        log_enabled = self.window.uic.cbox_log_settings_enable.isChecked()

        levels = []
        if log_error:
            levels.append(LogLevel.ERROR)
        if log_warning:
            levels.append(LogLevel.WARNING)
        if log_info:
            levels.append(LogLevel.INFO)
        if log_debug:
            levels.append(LogLevel.DEBUG)

        self.ring_manager.set_log_settings(
            self.devices[0].address,
            LogSettings(enable=log_enabled, levels=levels),
            self.on_log_settings_success
        )

    def on_log_settings_success(self, result: CommonResult):
        logger.info(f"Result: {result}")

    # BLE settings
    def set_bluetooth_settings(self):
        adv_name = self.window.uic.input_ble_settings_adv_name.text()
        adv_interval = float(self.window.uic.input_ble_settings_adv_interval.text())
        connection_interval_min = float(self.window.uic.input_ble_settings_conn_int_min.text())
        connection_interval_max = float(self.window.uic.input_ble_settings_conn_int_max.text())
        slave_latency = float(self.window.uic.input_ble_settings_slave_latency.text())
        supervision_time_out = float(self.window.uic.input_ble_settings_supervision_time_out.text())
        transmit_power_level = self.window.uic.box_ble_settings_tx_power_level.currentData()

        self.ring_manager.set_bluetooth_settings(
            self.devices[0].address,
            BTSettings(
                adv_name=adv_name,
                adv_interval=adv_interval,
                connection_interval_min=connection_interval_min,
                connection_interval_max=connection_interval_max,
                slave_latency=slave_latency,
                supervision_timeout=supervision_time_out,
                transmit_power_level=transmit_power_level,
            ),
            self.on_bluetooth_settings_set,
        )

    def on_bluetooth_settings_set(self, result: CommonResult):
        logger.info(f"Result: {result}")

    # Get all settings
    def get_all_settings(self):
        self.ring_manager.get_all_settings(self.connected_client.address, self.on_all_settings_received)

    def on_all_settings_received(self, result: CommonResult, settings: Optional[DeviceSettings]):
        if not result.is_success:
            logger.error(f"Result: {result}")
            return

        # ECG settings
        self.window.uic.ecg_settings_enabled.setChecked(settings.ecg_settings.enable)
        ecg_settings_sampling_index = self.window.uic.box_ecg_settings_sampling_rate.findData(
            settings.ecg_settings.sampling_rate)
        self.window.uic.box_ecg_settings_sampling_rate.setCurrentIndex(ecg_settings_sampling_index)
        ecg_settings_pga_gain_index = self.window.uic.box_ecg_settings_pga_gain.findData(settings.ecg_settings.pga_gain)
        self.window.uic.box_ecg_settings_pga_gain.setCurrentIndex(ecg_settings_pga_gain_index)
        ecg_settings_ina_gain_index = self.window.uic.box_ecg_settings_ina_gain.findData(settings.ecg_settings.ina_gain)
        self.window.uic.box_ecg_settings_ina_gain.setCurrentIndex(ecg_settings_ina_gain_index)
        ecg_settings_ina_range_index = self.window.uic.box_ecg_settings_ina_range.findData(
            settings.ecg_settings.ina_range)
        self.window.uic.box_ecg_settings_ina_range.setCurrentIndex(ecg_settings_ina_range_index)
        ecg_settings_input_polarity_index = self.window.uic.box_ecg_settings_input_polarity.findData(
            settings.ecg_settings.input_polarity)
        self.window.uic.box_ecg_settings_input_polarity.setCurrentIndex(ecg_settings_input_polarity_index)

        # Lead off settings
        self.window.uic.lead_off_settings_enabled.setChecked(settings.ecg_settings.lead_off_enable)
        lead_off_settings_mode_index = self.window.uic.box_lead_off_settings_mode.findData(
            settings.ecg_settings.lead_off_settings.mode)
        self.window.uic.box_lead_off_settings_mode.setCurrentIndex(lead_off_settings_mode_index)
        lead_off_settings_current_polarity_index = self.window.uic.box_lead_off_settings_current_polarity.findData(
            settings.ecg_settings.lead_off_settings.current_polarity)
        self.window.uic.box_lead_off_settings_current_polarity.setCurrentIndex(lead_off_settings_current_polarity_index)
        lead_off_settings_current_magnitude_index = self.window.uic.box_lead_off_settings_current_magnitude.findData(
            settings.ecg_settings.lead_off_settings.current_magnitude)
        self.window.uic.box_lead_off_settings_current_magnitude.setCurrentIndex(
            lead_off_settings_current_magnitude_index)
        lead_off_settings_voltage_threshold_index = self.window.uic.box_lead_off_settings_current_threshold.findData(
            settings.ecg_settings.lead_off_settings.voltage_threshold)
        self.window.uic.box_lead_off_settings_current_threshold.setCurrentIndex(
            lead_off_settings_voltage_threshold_index)
        lead_off_settings_frequency_index = self.window.uic.box_lead_off_settings_frequency.findData(
            settings.ecg_settings.lead_off_settings.lead_off_frequency)
        self.window.uic.box_lead_off_settings_frequency.setCurrentIndex(lead_off_settings_frequency_index)

        # ACCEL settings
        self.window.uic.accel_settings_enabled.setChecked(settings.accel_settings.enable)
        accel_settings_sampling_rate_index = self.window.uic.box_accel_settings_sampling_rate.findData(
            settings.accel_settings.sampling_rate)
        self.window.uic.box_accel_settings_sampling_rate.setCurrentIndex(accel_settings_sampling_rate_index)
        accel_settings_full_scale_range_index = self.window.uic.box_accel_settings_full_scale_range.findData(
            settings.accel_settings.full_scale_range)
        self.window.uic.box_accel_settings_full_scale_range.setCurrentIndex(accel_settings_full_scale_range_index)

        # PPG settings
        self.window.uic.ppg_settings_enabled.setChecked(settings.ppg_settings.enable)
        self.window.uic.ppg_settings_red_led_enabled.setChecked(settings.ppg_settings.enable_red_led)
        self.window.uic.ppg_settings_ir_led_enabled.setChecked(settings.ppg_settings.enable_ir_led)
        self.window.uic.input_red_led_current.setText(str(settings.ppg_settings.red_led_current))
        self.window.uic.input_ir_led_current.setText(str(settings.ppg_settings.ir_led_current))

        # Log settings
        self.window.uic.cbox_log_settings_enable.setChecked(settings.log_settings.enable)
        self.window.uic.cbox_log_settings_error.setChecked(LogLevel.ERROR in settings.log_settings.levels)
        self.window.uic.cbox_log_settings_warning.setChecked(LogLevel.WARNING in settings.log_settings.levels)
        self.window.uic.cbox_log_settings_info.setChecked(LogLevel.INFO in settings.log_settings.levels)
        self.window.uic.cbox_log_settings_debug.setChecked(LogLevel.DEBUG in settings.log_settings.levels)

        # BLE settings
        self.window.uic.input_ble_settings_adv_name.setText(settings.bluetooth_settings.adv_name)
        self.window.uic.input_ble_settings_adv_interval.setText(str(settings.bluetooth_settings.adv_interval))
        self.window.uic.input_ble_settings_conn_int_min.setText(str(settings.bluetooth_settings.connection_interval_min))
        self.window.uic.input_ble_settings_conn_int_max.setText(str(settings.bluetooth_settings.connection_interval_max))
        self.window.uic.input_ble_settings_slave_latency.setText(str(settings.bluetooth_settings.slave_latency))
        self.window.uic.input_ble_settings_supervision_time_out.setText(str(settings.bluetooth_settings.supervision_timeout))
        ble_settings_tx_power_level_index = self.window.uic.box_ble_settings_tx_power_level.findData(
            settings.bluetooth_settings.transmit_power_level)
        self.window.uic.box_ble_settings_tx_power_level.setCurrentIndex(ble_settings_tx_power_level_index)

    """ Self test """

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
        item = QListWidgetItem()
        item.setData(QListItemRole.data.value, data)
        item.setText(f"start_time:{data.start_time} - x:{data.x} - y:{data.y} - z:{data.z} - is_eot: {data.is_eot}")
        self.window.uic.recorded_data_list.addItem(item)

    def on_ecg_recorded(self, device: BTDevice, data: EcgData):
        item = QListWidgetItem()
        item.setData(QListItemRole.data.value, data)
        item.setText(f"start_time:{data.start_time} - ecg:{data.data} - is_eot: {data.is_eot}")
        self.window.uic.recorded_data_list.addItem(item)

    def on_ppg_recorded(self, device: BTDevice, data: PpgData):
        logger.info(f'device: {device}, data: {data}')

    def on_temp_recorded(self, device: BTDevice, data: TempData):
        logger.info(f'device: {device}, data: {data}')

    def on_record_error(self, device: BTDevice, data: CommonError):
        logger.info(f'device: {device}, data: {data}')

    def start_record(self):
        try:
            sensor_type = self.window.uic.start_record_sensor_type.currentData()
            samples = int(self.window.uic.input_samples.text())
            match sensor_type:
                case SensorType.PPG:
                    self.start_record_ppg(samples)
                case SensorType.ECG:
                    self.start_record_ecg(samples)
                case SensorType.ACCEL:
                    self.start_record_acc(samples)
                case SensorType.TEMP:
                    self.start_record_temp(samples)
                case _:
                    pass
        except Exception as e:
            logger.error(f"Invalid samples input: {e}")

    def start_record_ppg(self, samples: int):
        self.ring_manager.start_record(
            self.connected_client.address,
            samples, SensorType.PPG,
            self.on_start_record_ppg_success
        )

    def start_record_ecg(self, samples: int):
        self.ring_manager.start_record(
            self.connected_client.address,
            samples, SensorType.ECG,
            self.on_start_record_ecg_success
        )

    def start_record_acc(self, samples: int):
        self.ring_manager.start_record(
            self.connected_client.address,
            samples, SensorType.ACCEL,
            self.on_start_record_acc_success
        )

    def start_record_temp(self, samples: int):
        self.ring_manager.start_record(
            self.connected_client.address,
            samples, SensorType.TEMP,
            self.on_start_record_temp_success
        )

    def on_start_record_ppg_success(self, result: CommonResult):
        logger.info(f"on_record_ppf_success Result: {result}")

    def on_start_record_ecg_success(self, result: CommonResult):
        logger.info(f"on_record_ecg_success Result: {result}")

    def on_start_record_acc_success(self, result: CommonResult):
        logger.info(f"on_record_acc_success Result: {result}")

    def on_start_record_temp_success(self, result: CommonResult):
        logger.info(f"on_record_temp_success Result: {result}")

    def stop_record(self):
        sensor_type = self.window.uic.stop_record_sensor_type.currentData()

        match sensor_type:
            case SensorType.PPG:
                self.stop_record_ppg()
            case SensorType.ECG:
                self.stop_record_ecg()
            case SensorType.ACCEL:
                self.stop_record_acc()
            case SensorType.TEMP:
                self.stop_record_temp()
            case _:
                pass

    def stop_record_ecg(self):
        self.ring_manager.stop_record(self.connected_client.address, SensorType.ECG, self.on_stop_record_ecg_success)

    def on_stop_record_ecg_success(self, result: CommonResult):
        logger.info(f"on_stop_record_ecg_success Result: {result}")

    def stop_record_ppg(self):
        self.ring_manager.stop_record(self.connected_client.address, SensorType.PPG, self.on_stop_record_ppg_success)

    def on_stop_record_ppg_success(self, result: CommonResult):
        logger.info(f"on_stop_record_ppg_success Result: {result}")

    def stop_record_acc(self):
        self.ring_manager.stop_record(self.connected_client.address, SensorType.ACCEL, self.on_stop_record_acc_success)

    def on_stop_record_acc_success(self, result: CommonResult):
        logger.info(f"on_stop_record_acc_success Result: {result}")

    def stop_record_temp(self):
        self.ring_manager.stop_record(self.connected_client.address, SensorType.TEMP, self.on_stop_record_temp_success)

    def on_stop_record_temp_success(self, result: CommonResult):
        logger.info(f"on_stop_record_temp_success Result: {result}")

    def get_record(self):
        try:
            sensor_type = self.window.uic.get_record_sensor_type.currentData()
            start_index = int(self.window.uic.input_get_record_start_index.text())
            match sensor_type:
                case SensorType.PPG:
                    self.get_record_ppg(start_index)
                case SensorType.ECG:
                    self.get_record_ecg(start_index)
                case SensorType.ACCEL:
                    self.get_record_acc(start_index)
                case SensorType.TEMP:
                    self.get_record_temp(start_index)
                case _:
                    pass
        except Exception as e:
            logger.error(f"Invalid start index input: {e}")

    def get_record_ppg(self, start_index: int):
        self.ring_manager.get_record(self.connected_client.address, SensorType.PPG, start_index)

    def get_record_ecg(self, start_index: int):
        self.ring_manager.get_record(self.connected_client.address, SensorType.ECG, start_index)

    def get_record_acc(self, start_index: int):
        self.ring_manager.get_record(self.connected_client.address, SensorType.ACCEL, start_index)

    def get_record_temp(self, start_index: int):
        self.ring_manager.get_record(self.connected_client.address, SensorType.TEMP, start_index)

    def on_get_record_success(self, result: CommonResult):
        logger.info(f"on_get_record_success Result: {result}")

    def get_record_samples_threshold(self):
        self.ring_manager.get_record_samples_threshold(self.connected_client.address,
                                                       self.on_get_record_samples_threshold)

    def on_get_record_samples_threshold(self, result: CommonResult, samples_threshold: Optional[SamplesThreshold]):
        if result.is_success:
            self.window.uic.sample_max_acc.setText(str(samples_threshold.max_accel_samples))
            self.window.uic.sample_max_ecg.setText(str(samples_threshold.max_ecg_samples))
            self.window.uic.sample_max_ppg.setText(str(samples_threshold.max_ppg_samples))
            self.window.uic.sample_max_temp.setText(str(samples_threshold.max_temp_samples))
            return
        logger.info(f"Result: {result}")

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
