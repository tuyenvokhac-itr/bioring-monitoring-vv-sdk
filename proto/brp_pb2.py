# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: brp.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    1,
    '',
    'brp.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tbrp.proto\x12\x03\x42RP\"-\n\x0cProtocolInfo\x12\x1d\n\x07version\x18\x01 \x02(\x04:\x0c\x32\x30\x32\x34\x30\x39\x32\x30\x31\x37\x30\x30\"\xdf\x01\n\x06Packet\x12\x0b\n\x03sid\x18\x01 \x02(\x04\x12\x1d\n\x04type\x18\x02 \x02(\x0e\x32\x0f.BRP.PacketType\x12%\n\x07\x63ommand\x18\x03 \x01(\x0b\x32\x12.BRP.CommandPacketH\x00\x12\'\n\x08response\x18\x04 \x01(\x0b\x32\x13.BRP.ResponsePacketH\x00\x12/\n\x0cnotification\x18\x05 \x01(\x0b\x32\x17.BRP.NotificationPacketH\x00\x12\x1d\n\x03\x61\x63k\x18\x06 \x01(\x0b\x32\x0e.BRP.AckPacketH\x00\x42\t\n\x07payload\"\xe9\x03\n\rCommandPacket\x12\x1b\n\x03\x63id\x18\x01 \x02(\x0e\x32\x0e.BRP.CommandId\x12!\n\x07mem_set\x18\x02 \x01(\x0b\x32\x0e.BRP.CmdMemSetH\x00\x12!\n\x07mem_get\x18\x03 \x01(\x0b\x32\x0e.BRP.CmdMemGetH\x00\x12\'\n\x0b\x61\x66\x65_setting\x18\x04 \x01(\x0b\x32\x10.BRP.AfeSettingsH\x00\x12+\n\x0ewlc_run_params\x18\x05 \x01(\x0b\x32\x11.BRP.WlcRunParamsH\x00\x12+\n\x0ewlc_oem_params\x18\x06 \x01(\x0b\x32\x11.BRP.WlcOemParamsH\x00\x12\x15\n\x0bsensor_type\x18\x07 \x01(\rH\x00\x12*\n\rsensor_config\x18\x08 \x01(\x0b\x32\x11.BRP.SensorConfigH\x00\x12\x17\n\rbist_interval\x18\t \x01(\rH\x00\x12\x17\n\rrecord_sample\x18\n \x01(\rH\x00\x12\x1b\n\x11pre_sleep_timeout\x18\x0c \x01(\rH\x00\x12$\n\ndev_status\x18\r \x01(\x0b\x32\x0e.BRP.DevStatusH\x00\x12/\n\x10\x61ll_dev_settings\x18\x0e \x01(\x0b\x32\x13.BRP.AllDevSettingsH\x00\x42\t\n\x07payload\"\xb4\x04\n\x0eResponsePacket\x12\x1b\n\x03\x63id\x18\x01 \x02(\x0e\x32\x0e.BRP.CommandId\x12!\n\x06result\x18\x02 \x02(\x0e\x32\x11.BRP.ResponseCode\x12*\n\rprotocol_info\x18\x04 \x01(\x0b\x32\x11.BRP.ProtocolInfoH\x00\x12!\n\x07mem_get\x18\x05 \x01(\x0b\x32\x0e.BRP.RspMemGetH\x00\x12 \n\x08\x64\x65v_info\x18\x06 \x01(\x0b\x32\x0c.BRP.DevInfoH\x00\x12\'\n\x0b\x61\x66\x65_setting\x18\x07 \x01(\x0b\x32\x10.BRP.AfeSettingsH\x00\x12+\n\x0ewlc_run_params\x18\x08 \x01(\x0b\x32\x11.BRP.WlcRunParamsH\x00\x12+\n\x0ewlc_oem_params\x18\t \x01(\x0b\x32\x11.BRP.WlcOemParamsH\x00\x12+\n\x0eself_test_data\x18\x0b \x01(\x0b\x32\x11.BRP.SelfTestDataH\x00\x12/\n\x10\x61ll_dev_settings\x18\r \x01(\x0b\x32\x13.BRP.AllDevSettingsH\x00\x12-\n\x0fppg_led_control\x18\x0e \x01(\x0b\x32\x12.BRP.PpgLedControlH\x00\x12$\n\ndev_status\x18\x0f \x01(\x0b\x32\x0e.BRP.DevStatusH\x00\x12\x30\n\x10sample_threshold\x18\x10 \x01(\x0b\x32\x14.BRP.SampleThresholdH\x00\x42\t\n\x07payload\"\x85\x02\n\x12NotificationPacket\x12 \n\x03nid\x18\x02 \x02(\x0e\x32\x13.BRP.NotificationId\x12\x0b\n\x03\x61\x63k\x18\x03 \x02(\x08\x12\x1b\n\x03log\x18\x04 \x01(\x0b\x32\x0c.BRP.NotiLogH\x00\x12\x12\n\x08\x63harging\x18\x05 \x01(\x08H\x00\x12\x17\n\rbattery_level\x18\x06 \x01(\rH\x00\x12\"\n\x07spo2_hr\x18\x07 \x01(\x0b\x32\x0f.BRP.Spo2HrDataH\x00\x12\x1d\n\x13\x65\x63g_lead_off_detect\x18\x08 \x01(\x08H\x00\x12(\n\x0b\x62ist_result\x18\t \x01(\x0b\x32\x11.BRP.SelfTestDataH\x00\x42\t\n\x07payload\"S\n\tAckPacket\x12 \n\x03nid\x18\x01 \x02(\x0e\x32\x13.BRP.NotificationId\x12$\n\x06result\x18\x02 \x02(\x0e\x32\x14.BRP.AckResponseCode\"\xbb\x01\n\x07\x44\x65vInfo\x12\x15\n\rserial_number\x18\x01 \x01(\t\x12\x1a\n\x12manufacturing_date\x18\x02 \x01(\t\x12\x0b\n\x03lot\x18\x03 \x01(\t\x12\r\n\x05model\x18\x04 \x01(\t\x12\x14\n\x0cpcba_version\x18\x05 \x01(\t\x12\x1a\n\x12\x62ootloader_version\x18\x06 \x01(\t\x12\x1b\n\x13\x61pplication_version\x18\x07 \x01(\t\x12\x12\n\nbuild_date\x18\x08 \x01(\t\":\n\tCmdMemSet\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x02(\r\x12\x0e\n\x06length\x18\x02 \x02(\r\x12\x0c\n\x04\x64\x61ta\x18\x03 \x02(\x0c\",\n\tCmdMemGet\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x02(\r\x12\x0e\n\x06length\x18\x02 \x02(\r\"\x19\n\tRspMemGet\x12\x0c\n\x04\x64\x61ta\x18\x01 \x02(\x0c\"\x17\n\x07NotiLog\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\t\"\xb7\t\n\x0b\x41\x66\x65Settings\x12\x17\n\x0f\x65\x63g_sample_rate\x18\x01 \x02(\r\x12\x17\n\x0fppg_sample_rate\x18\x02 \x02(\r\x12\x1e\n\x16ppg_meas1_current_step\x18\x03 \x02(\r\x12\x1e\n\x16ppg_meas2_current_step\x18\x04 \x02(\r\x12\x19\n\x11ppg_meas1_current\x18\x05 \x02(\x02\x12\x19\n\x11ppg_meas2_current\x18\x06 \x02(\x02\x12\x17\n\x0f\x65\x63g_input_polar\x18\x07 \x02(\r\x12\x14\n\x0c\x65\x63g_pga_gain\x18\x08 \x02(\r\x12\x14\n\x0c\x65\x63g_ina_gain\x18\t \x02(\r\x12\x1a\n\x12\x65\x63g_auto_reco_mode\x18\n \x02(\r\x12\x1f\n\x17\x65\x63g_auto_fast_reco_mode\x18\x0b \x02(\r\x12!\n\x19\x65\x63g_auto_fast_reco_thresh\x18\x0c \x02(\r\x12\x16\n\x0e\x65\x63g_rld_enable\x18\r \x02(\r\x12\x14\n\x0c\x65\x63g_rld_mode\x18\x0e \x02(\r\x12 \n\x18\x65\x63g_rld_pos_input_enable\x18\x0f \x02(\r\x12 \n\x18\x65\x63g_rld_neg_input_enable\x18\x10 \x02(\r\x12\x14\n\x0c\x65\x63g_rld_gain\x18\x11 \x02(\r\x12\x1e\n\x16\x65\x63g_rld_ex_res_connect\x18\x12 \x02(\r\x12\x1a\n\x12\x65\x63g_rld_select_ecg\x18\x13 \x02(\r\x12\x1c\n\x14ppg_meas1_inter_time\x18\x14 \x02(\r\x12\x1c\n\x14ppg_meas2_inter_time\x18\x15 \x02(\r\x12\x1d\n\x15ppg_meas1_pd_seltling\x18\x16 \x02(\r\x12\x1d\n\x15ppg_meas2_pd_seltling\x18\x17 \x02(\r\x12\x1e\n\x16ppg_meas1_led_seltling\x18\x18 \x02(\r\x12\x1e\n\x16ppg_meas2_led_seltling\x18\x19 \x02(\r\x12\x1d\n\x15ppg_meas1_ppg1_offset\x18\x1a \x02(\r\x12\x1d\n\x15ppg_meas2_ppg1_offset\x18\x1b \x02(\r\x12\x1d\n\x15ppg_meas1_ppg2_offset\x18\x1c \x02(\r\x12\x1d\n\x15ppg_meas2_ppg2_offset\x18\x1d \x02(\r\x12\x1e\n\x16ppg_meas1_sinc3_filter\x18\x1e \x02(\r\x12\x1e\n\x16ppg_meas2_sinc3_filter\x18\x1f \x02(\r\x12\x1c\n\x14ppg_meas1_alc_method\x18  \x02(\r\x12\x1c\n\x14ppg_meas2_alc_method\x18! \x02(\r\x12\x1e\n\x16ppg_meas1_filter_order\x18\" \x02(\r\x12\x1e\n\x16ppg_meas2_filter_order\x18# \x02(\r\x12\x19\n\x11ppg_meas1_ambient\x18$ \x02(\r\x12\x19\n\x11ppg_meas2_ambient\x18% \x02(\r\x12\x1f\n\x17ppg_pd1_photodiode_bias\x18& \x02(\r\x12\x1a\n\x12ppg_proximity_mode\x18\' \x02(\r\x12\x1d\n\x15ppg_threshold_1_lower\x18( \x02(\r\x12\x13\n\x0b\x65\x63g_ina_rge\x18) \x02(\r\"\xc8\x01\n\x0cWlcRunParams\x12\x16\n\x0e\x63harge_current\x18\x01 \x02(\r\x12\x18\n\x10recharge_voltage\x18\x02 \x02(\r\x12\x1b\n\x13termination_voltage\x18\x03 \x02(\r\x12\x17\n\x0ftrickle_voltage\x18\x04 \x02(\r\x12\x17\n\x0f\x65nable_charging\x18\x05 \x02(\r\x12\x0f\n\x07wpt_req\x18\x06 \x02(\r\x12\x14\n\x0cwpt_duration\x18\x07 \x02(\r\x12\x10\n\x08\x64\x65tuning\x18\x08 \x02(\r\"\xd0\x07\n\x0cWlcOemParams\x12\x18\n\x10\x62\x63_i_charge_cold\x18\x01 \x02(\r\x12\x17\n\x0f\x62\x63_i_charge_hot\x18\x02 \x02(\r\x12\x11\n\tbc_v_term\x18\x03 \x02(\r\x12\x16\n\x0e\x62\x63_v_term_cold\x18\x04 \x02(\r\x12\x15\n\rbc_v_term_hot\x18\x05 \x02(\r\x12\x14\n\x0c\x62\x63_v_trickle\x18\x06 \x02(\r\x12\x15\n\rbc_v_recharge\x18\x07 \x02(\r\x12\x13\n\x0bvd_mcu_mode\x18\x08 \x02(\r\x12\x17\n\x0fi_sensor_thresh\x18\t \x02(\r\x12\x1c\n\x14\x61\x64j_wpt_duration_int\x18\n \x02(\r\x12\x1c\n\x14tcm_wpt_duration_int\x18\x0b \x02(\r\x12\x1c\n\x14\x63\x63m_wpt_duration_int\x18\x0c \x02(\r\x12\x1c\n\x14\x63vm_wpt_duration_int\x18\r \x02(\r\x12\x12\n\ncap_wt_int\x18\x0e \x02(\r\x12\x14\n\x0cgpio0_config\x18\x0f \x02(\r\x12\x14\n\x0cgpio1_config\x18\x10 \x02(\r\x12\x16\n\x0e\x62\x63_uvlo_thresh\x18\x11 \x02(\r\x12\x13\n\x0bwpt_req_sel\x18\x12 \x02(\r\x12\x14\n\x0cirq_polarity\x18\x13 \x02(\r\x12\x19\n\x11nfc_resistive_mod\x18\x14 \x02(\r\x12\x19\n\x11nfc_resistive_set\x18\x15 \x02(\r\x12\x19\n\x11wpt_resistive_mod\x18\x16 \x02(\r\x12\x19\n\x11wpt_resistive_set\x18\x17 \x02(\r\x12\x10\n\x08ntc_mode\x18\x18 \x02(\r\x12\x17\n\x0f\x62\x63_i_charge_wpt\x18\x19 \x02(\r\x12\x17\n\x0f\x62\x63_i_charge_nfc\x18\x1a \x02(\r\x12\x11\n\tbc_i_term\x18\x1b \x02(\r\x12\x14\n\x0c\x62\x63_i_lim_sel\x18\x1c \x02(\r\x12\x1b\n\x13\x62\x63_i_lim_bat_enable\x18\x1d \x02(\r\x12\x18\n\x10\x62\x63_lo_bat_off_en\x18\x1e \x02(\r\x12\x11\n\tbc_enable\x18\x1f \x02(\r\x12\x13\n\x0bi2c_address\x18  \x02(\r\x12\x13\n\x0btcm_timeout\x18! \x02(\r\x12\x13\n\x0b\x63\x63m_timeout\x18\" \x02(\r\x12\x13\n\x0b\x63vm_timeout\x18# \x02(\r\x12\x16\n\x0evddc_thres_low\x18$ \x02(\r\x12\x1a\n\x12vd_bat_offset_high\x18% \x02(\r\x12\x19\n\x11vd_bat_offset_low\x18& \x02(\r\x12\x1a\n\x12\x64\x63_charging_enable\x18\' \x02(\r\x12\x13\n\x0boem_version\x18( \x02(\r\"S\n\x0cSensorConfig\x12$\n\x0bsensor_type\x18\x01 \x01(\x0e\x32\x0f.BRP.SensorType\x12\x1d\n\x04mode\x18\x02 \x01(\x0e\x32\x0f.BRP.SensorMode\".\n\nSpo2HrData\x12\x10\n\x04spo2\x18\x01 \x03(\rB\x02\x10\x01\x12\x0e\n\x02hr\x18\x02 \x03(\rB\x02\x10\x01\"m\n\x0cSelfTestData\x12\x0b\n\x03\x61\x66\x65\x18\x01 \x01(\x08\x12\r\n\x05\x61\x63\x63\x65l\x18\x02 \x01(\x08\x12\x13\n\x0btemperature\x18\x03 \x01(\x08\x12\x18\n\x10wireless_charger\x18\x04 \x01(\x08\x12\x12\n\nfuel_gauge\x18\x05 \x01(\x08\"\xb4\x02\n\tDevStatus\x12!\n\x0b\x63urrent_app\x18\x01 \x01(\x0e\x32\x0c.BRP.AppType\x12\x13\n\x0b\x64\x65vice_time\x18\x02 \x01(\r\x12&\n\x0b\x62ist_result\x18\x03 \x01(\x0b\x32\x11.BRP.SelfTestData\x12\x16\n\x0e\x62ist_timestamp\x18\x04 \x01(\r\x12&\n\x0bpost_result\x18\x05 \x01(\x0b\x32\x11.BRP.SelfTestData\x12\x16\n\x0epost_timestamp\x18\x06 \x01(\r\x12,\n\x0f\x63harging_status\x18\x07 \x01(\x0e\x32\x13.BRP.ChargingStatus\x12*\n\x0e\x63harging_error\x18\x08 \x01(\x0e\x32\x12.BRP.ChargingError\x12\x15\n\rbattery_level\x18\t \x01(\r\"\"\n\x0fPowerManagement\x12\x0f\n\x07timeout\x18\x01 \x01(\r\"x\n\x0fSampleThreshold\x12\x19\n\x11max_accel_samples\x18\x01 \x01(\r\x12\x17\n\x0fmax_ecg_samples\x18\x02 \x01(\r\x12\x17\n\x0fmax_ppg_samples\x18\x03 \x01(\r\x12\x18\n\x10max_temp_samples\x18\x04 \x01(\r\"z\n\x10\x42leConnectParams\x12\x18\n\x10\x63onnect_intv_min\x18\x01 \x01(\x02\x12\x18\n\x10\x63onnect_intv_max\x18\x02 \x01(\x02\x12\x15\n\rslave_latency\x18\x03 \x01(\r\x12\x1b\n\x13supervision_timeout\x18\x04 \x01(\r\"\xa2\x01\n\x0b\x42leSettings\x12\x18\n\x10\x61\x64vertising_name\x18\x01 \x01(\t\x12\x1c\n\x14\x61\x64vertising_interval\x18\x02 \x01(\x02\x12-\n\x0e\x63onnect_params\x18\x03 \x01(\x0b\x32\x15.BRP.BleConnectParams\x12,\n\x0etx_power_level\x18\x04 \x01(\x0e\x32\x14.BRP.BleTxPowerLevel\"C\n\x0bLogSettings\x12\x12\n\nlog_enable\x18\x01 \x01(\x08\x12 \n\tlog_level\x18\x02 \x01(\x0e\x32\r.BRP.LogLevel\"t\n\x07\x45\x63gGain\x12!\n\x08pga_gain\x18\x01 \x01(\x0e\x32\x0f.BRP.EcgPgaGain\x12!\n\x08ina_gain\x18\x02 \x01(\x0e\x32\x0f.BRP.EcgInaGain\x12#\n\tina_range\x18\x03 \x01(\x0e\x32\x10.BRP.EcgInaRange\"\xb7\x02\n\x10\x45\x63gLeadOffParams\x12*\n\rlead_off_mode\x18\x01 \x01(\x0e\x32\x13.BRP.EcgLeadOffMode\x12\x41\n\x19lead_off_current_polarity\x18\x02 \x01(\x0e\x32\x1e.BRP.EcgLeadOffCurrentPolarity\x12\x43\n\x1alead_off_current_magnitude\x18\x03 \x01(\x0e\x32\x1f.BRP.EcgLeadOffCurrentMagnitude\x12\x43\n\x1alead_off_voltage_threshold\x18\x04 \x01(\x0e\x32\x1f.BRP.EcgLeadOffVoltageThreshold\x12*\n\rlead_off_freq\x18\x05 \x01(\x0e\x32\x13.BRP.EcgLeadOffFreq\"\xe2\x01\n\x0b\x45\x63gSettings\x12\x12\n\necg_enable\x18\x01 \x01(\x08\x12\'\n\x0bsample_rate\x18\x02 \x01(\x0e\x32\x12.BRP.EcgSampleRate\x12\x1e\n\x08\x65\x63g_gain\x18\x03 \x01(\x0b\x32\x0c.BRP.EcgGain\x12-\n\x0einput_polarity\x18\x04 \x01(\x0e\x32\x15.BRP.EcgInputPolarity\x12\x17\n\x0flead_off_enable\x18\x05 \x01(\x08\x12.\n\x0flead_off_params\x18\x06 \x01(\x0b\x32\x15.BRP.EcgLeadOffParams\"6\n\rPpgLedControl\x12%\n\x0cppg_led_type\x18\x01 \x01(\x0e\x32\x0f.BRP.PpgLedType\"p\n\x0ePpgLedSettings\x12\x16\n\x0ered_led_enable\x18\x01 \x01(\x08\x12\x15\n\rir_led_enable\x18\x02 \x01(\x08\x12\x17\n\x0fred_led_current\x18\x03 \x01(\x02\x12\x16\n\x0eir_led_current\x18\x04 \x01(\x02\"y\n\x0bPpgSettings\x12\x12\n\nppg_enable\x18\x01 \x01(\x08\x12\'\n\x0bsample_rate\x18\x02 \x01(\x0e\x32\x12.BRP.PpgSampleRate\x12-\n\x10ppg_led_settings\x18\x03 \x01(\x0b\x32\x13.BRP.PpgLedSettings\"\x7f\n\rAccelSettings\x12\x14\n\x0c\x61\x63\x63\x65l_enable\x18\x01 \x01(\x08\x12)\n\x0bsample_rate\x18\x02 \x01(\x0e\x32\x14.BRP.AccelSampleRate\x12-\n\x10\x61\x63\x63\x65l_full_scale\x18\x03 \x01(\x0e\x32\x13.BRP.AccelFullScale\"\xdc\x01\n\x0e\x41llDevSettings\x12&\n\x0c\x65\x63g_settings\x18\x02 \x01(\x0b\x32\x10.BRP.EcgSettings\x12&\n\x0cppg_settings\x18\x03 \x01(\x0b\x32\x10.BRP.PpgSettings\x12*\n\x0e\x61\x63\x63\x65l_settings\x18\x04 \x01(\x0b\x32\x12.BRP.AccelSettings\x12&\n\x0c\x62le_settings\x18\x05 \x01(\x0b\x32\x10.BRP.BleSettings\x12&\n\x0clog_settings\x18\x06 \x01(\x0b\x32\x10.BRP.LogSettings*\x8f\x01\n\nPacketType\x12\x1b\n\x17PACKET_TYPE_UNSPECIFIED\x10\x00\x12\x17\n\x13PACKET_TYPE_COMMAND\x10\x01\x12\x18\n\x14PACKET_TYPE_RESPONSE\x10\x02\x12\x1c\n\x18PACKET_TYPE_NOTIFICATION\x10\x03\x12\x13\n\x0fPACKET_TYPE_ACK\x10\x04*c\n\nSensorType\x12\x13\n\x0fSENSOR_TYPE_PPG\x10\x01\x12\x13\n\x0fSENSOR_TYPE_ECG\x10\x02\x12\x15\n\x11SENSOR_TYPE_ACCEL\x10\x04\x12\x14\n\x10SENSOR_TYPE_TEMP\x10\x08*\x8f\n\n\tCommandId\x12\x13\n\x0f\x43ID_UNSPECIFIED\x10\x00\x12\x10\n\x0c\x43ID_TIME_SET\x10\x01\x12\x10\n\x0c\x43ID_TIME_GET\x10\x02\x12\x19\n\x15\x43ID_PROTOCOL_INFO_GET\x10\x03\x12\x14\n\x10\x43ID_DEV_INFO_GET\x10\x04\x12\x16\n\x12\x43ID_DEV_STATUS_GET\x10\x05\x12\x1a\n\x16\x43ID_SELF_TEST_POST_GET\x10\x06\x12\x1a\n\x16\x43ID_SELF_TEST_BIST_GET\x10\x07\x12\x1d\n\x19\x43ID_SELF_TEST_BIST_ENABLE\x10\x08\x12\x1e\n\x1a\x43ID_SELF_TEST_BIST_DISABLE\x10\t\x12#\n\x1f\x43ID_SELF_TEST_BIST_SET_INTERVAL\x10\n\x12\x1c\n\x18\x43ID_STREAMING_DATA_START\x10\x0b\x12\x1b\n\x17\x43ID_STREAMING_DATA_STOP\x10\x0c\x12$\n CID_RECORD_SAMPLES_THRESHOLD_GET\x10\r\x12\x19\n\x15\x43ID_RECORD_DATA_START\x10\x0e\x12\x18\n\x14\x43ID_RECORD_DATA_STOP\x10\x0f\x12\x17\n\x13\x43ID_RECORD_DATA_GET\x10\x10\x12\x18\n\x14\x43ID_ALL_SETTINGS_GET\x10\x11\x12\x18\n\x14\x43ID_ALL_SETTINGS_SET\x10\x12\x12\x18\n\x14\x43ID_ECG_SETTINGS_SET\x10\x13\x12\x18\n\x14\x43ID_PPG_SETTINGS_SET\x10\x14\x12\x1a\n\x16\x43ID_ACCEL_SETTINGS_SET\x10\x15\x12\x18\n\x14\x43ID_BLE_SETTINGS_SET\x10\x16\x12\x18\n\x14\x43ID_LOG_SETTINGS_SET\x10\x17\x12\x11\n\rCID_DFU_ENTER\x10\x18\x12!\n\x1d\x43ID_DEV_PRE_SLEEP_TIMEOUT_SET\x10\x19\x12\x19\n\x15\x43ID_DEV_FACTORY_RESET\x10\x1a\x12\x0e\n\nCID_REBOOT\x10\x1b\x12\x0f\n\x0b\x43ID_MEM_SET\x10\x1c\x12\x0f\n\x0b\x43ID_MEM_GET\x10\x1d\x12\x1e\n\x1a\x43ID_AFE_SENSOR_SETTING_SET\x10\x1e\x12\x1e\n\x1a\x43ID_AFE_SENSOR_SETTING_GET\x10\x1f\x12\x1a\n\x16\x43ID_WLC_RUN_PARAMS_SET\x10 \x12\x1a\n\x16\x43ID_WLC_RUN_PARAMS_GET\x10!\x12\x1a\n\x16\x43ID_WLC_OEM_PARAMS_SET\x10\"\x12\x1a\n\x16\x43ID_WLC_OEM_PARAMS_GET\x10#\x12\x15\n\x11\x43ID_SPO2_HR_START\x10$\x12\x14\n\x10\x43ID_SPO2_HR_STOP\x10%\x12\x11\n\rCID_DEV_SLEEP\x10&\x12\x12\n\x0e\x43ID_DEV_REINIT\x10\'\x12\x16\n\x11\x43ID_BLE_DTM_LE_TX\x10\xf8\x01\x12\x1b\n\x16\x43ID_BLE_DTM_LE_TX_RESP\x10\xf9\x01\x12\x16\n\x11\x43ID_BLE_DTM_LE_RX\x10\xfa\x01\x12\x1b\n\x16\x43ID_BLE_DTM_LE_RX_RESP\x10\xfb\x01\x12\x1f\n\x1a\x43ID_BLE_DTM_UNMODULATED_TX\x10\xfc\x01\x12$\n\x1f\x43ID_BLE_DTM_UNMODULATED_TX_RESP\x10\xfd\x01\x12\x1f\n\x1a\x43ID_BLE_DTM_UNMODULATED_RX\x10\xfe\x01\x12$\n\x1f\x43ID_BLE_DTM_UNMODULATED_RX_RESP\x10\xff\x01*\xcd\x01\n\x0cResponseCode\x12\x12\n\x0eRC_UNSPECIFIED\x10\x00\x12\t\n\x05RC_OK\x10\x01\x12\x1a\n\x16RC_ERROR_UNIMPLEMENTED\x10\x02\x12\x17\n\x13RC_ERROR_CMD_FAILED\x10\x03\x12\x16\n\x12RC_ERROR_TIMED_OUT\x10\x04\x12\x11\n\rRC_ERROR_BUSY\x10\x05\x12 \n\x1cRC_ERROR_INVALID_PACKET_TYPE\x10\x06\x12\x1c\n\x18RC_ERROR_INVALID_PAYLOAD\x10\x07*\xbf\x01\n\x0eNotificationId\x12\x13\n\x0fNID_UNSPECIFIED\x10\x00\x12\x10\n\x0cNID_LOG_DATA\x10\x01\x12\x1f\n\x1bNID_CHARGING_STATUS_CHANGED\x10\x02\x12\x1d\n\x19NID_BATTERY_LEVEL_CHANGED\x10\x03\x12\x14\n\x10NID_SPO2_HR_DATA\x10\x04\x12\x1b\n\x17NID_ECG_LEAD_OFF_DETECT\x10\x05\x12\x13\n\x0fNID_BIST_RESULT\x10\x06*\xeb\x01\n\x0f\x41\x63kResponseCode\x12\x16\n\x12\x41\x43K_RC_UNSPECIFIED\x10\x00\x12\x0e\n\nACK_RC_ACK\x10\x01\x12\x1d\n\x19\x41\x43K_RC_NACK_UNIMPLEMENTED\x10\x02\x12\x1a\n\x16\x41\x43K_RC_NACK_CMD_FAILED\x10\x03\x12\x19\n\x15\x41\x43K_RC_NACK_TIMED_OUT\x10\x04\x12\x14\n\x10\x41\x43K_RC_NACK_BUSY\x10\x05\x12#\n\x1f\x41\x43K_RC_NACK_INVALID_PACKET_TYPE\x10\x06\x12\x1f\n\x1b\x41\x43K_RC_NACK_INVALID_PAYLOAD\x10\x07*<\n\x07\x41ppType\x12\x17\n\x13\x41PP_TYPE_BOOTLOADER\x10\x00\x12\x18\n\x14\x41PP_TYPE_APPLICATION\x10\x01*m\n\nSensorMode\x12\x0f\n\x0bSM_MODE_OFF\x10\x01\x12\x12\n\x0eSM_MODE_STREAM\x10\x02\x12\x1b\n\x17SM_MODE_RECORD_TO_FLASH\x10\x03\x12\x1d\n\x19SM_MODE_UPLOAD_FROM_FLASH\x10\x04*_\n\x08LogLevel\x12\x13\n\x0fLOG_LEVEL_ERROR\x10\x00\x12\x15\n\x11LOG_LEVEL_WARNING\x10\x01\x12\x12\n\x0eLOG_LEVEL_INFO\x10\x02\x12\x13\n\x0fLOG_LEVEL_DEBUG\x10\x03*O\n\x0e\x43hargingStatus\x12\x1f\n\x1b\x43HARGING_STATUS_DISCHARGING\x10\x00\x12\x1c\n\x18\x43HARGING_STATUS_CHARGING\x10\x01*\xfe\x01\n\rChargingError\x12\x15\n\x11\x43HARGING_ERROR_OK\x10\x00\x12\x1a\n\x16\x43HARGING_ERROR_IC_TEMP\x10\x01\x12\x1b\n\x17\x43HARGING_ERROR_PROTOCOL\x10\x02\x12\x1f\n\x1b\x43HARGING_ERROR_BATT_CONNECT\x10\x04\x12\x1c\n\x18\x43HARGING_ERROR_BATT_TEMP\x10\x08\x12\x1e\n\x1a\x43HARGING_ERROR_TCM_TIMEOUT\x10\x0c\x12\x1e\n\x1a\x43HARGING_ERROR_CCM_TIMEOUT\x10\x10\x12\x1e\n\x1a\x43HARGING_ERROR_CVM_TIMEOUT\x10\x14*\xe4\x01\n\x0f\x42leTxPowerLevel\x12&\n\x19\x42LE_TX_POWER_LEVEL_NEG_20\x10\xec\xff\xff\xff\xff\xff\xff\xff\xff\x01\x12&\n\x19\x42LE_TX_POWER_LEVEL_NEG_16\x10\xf0\xff\xff\xff\xff\xff\xff\xff\xff\x01\x12&\n\x19\x42LE_TX_POWER_LEVEL_NEG_12\x10\xf4\xff\xff\xff\xff\xff\xff\xff\xff\x01\x12%\n\x18\x42LE_TX_POWER_LEVEL_NEG_6\x10\xfa\xff\xff\xff\xff\xff\xff\xff\xff\x01\x12\x18\n\x14\x42LE_TX_POWER_LEVEL_0\x10\x00\x12\x18\n\x14\x42LE_TX_POWER_LEVEL_4\x10\x04*_\n\rEcgSampleRate\x12\x18\n\x14\x45\x43G_SAMPLE_RATE_64HZ\x10\x00\x12\x19\n\x15\x45\x43G_SAMPLE_RATE_128HZ\x10\x01\x12\x19\n\x15\x45\x43G_SAMPLE_RATE_256HZ\x10\x02*q\n\nEcgPgaGain\x12\x12\n\x0e\x45\x43G_PGA_GAIN_1\x10\x00\x12\x12\n\x0e\x45\x43G_PGA_GAIN_2\x10\x01\x12\x12\n\x0e\x45\x43G_PGA_GAIN_4\x10\x02\x12\x12\n\x0e\x45\x43G_PGA_GAIN_8\x10\x03\x12\x13\n\x0f\x45\x43G_PGA_GAIN_16\x10\x07*\\\n\nEcgInaGain\x12\x12\n\x0e\x45\x43G_INA_GAIN_0\x10\x00\x12\x12\n\x0e\x45\x43G_INA_GAIN_1\x10\x01\x12\x12\n\x0e\x45\x43G_INA_GAIN_2\x10\x02\x12\x12\n\x0e\x45\x43G_INA_GAIN_3\x10\x03*m\n\x0b\x45\x63gInaRange\x12\x16\n\x12\x45\x43G_INA_GAIN_RGE_0\x10\x00\x12\x16\n\x12\x45\x43G_INA_GAIN_RGE_1\x10\x01\x12\x16\n\x12\x45\x43G_INA_GAIN_RGE_2\x10\x02\x12\x16\n\x12\x45\x43G_INA_GAIN_RGE_3\x10\x03*F\n\x10\x45\x63gInputPolarity\x12\x1a\n\x16\x45\x43G_INPUT_NON_INVERTED\x10\x00\x12\x16\n\x12\x45\x43G_INPUT_INVERTED\x10\x01*:\n\x0e\x45\x63gLeadOffMode\x12\x13\n\x0f\x45\x43G_LEAD_OFF_DC\x10\x00\x12\x13\n\x0f\x45\x43G_LEAD_OFF_AC\x10\x01*U\n\x19\x45\x63gLeadOffCurrentPolarity\x12\x1d\n\x19\x45\x43G_LEAD_OFF_NON_INVERTED\x10\x00\x12\x19\n\x15\x45\x43G_LEAD_OFF_INVERTED\x10\x01*\xed\x01\n\x1a\x45\x63gLeadOffCurrentMagnitude\x12\x17\n\x13\x45\x43G_LEAD_OFF_IMAG_0\x10\x00\x12\x17\n\x13\x45\x43G_LEAD_OFF_IMAG_5\x10\x01\x12\x18\n\x14\x45\x43G_LEAD_OFF_IMAG_10\x10\x02\x12\x18\n\x14\x45\x43G_LEAD_OFF_IMAG_20\x10\x03\x12\x18\n\x14\x45\x43G_LEAD_OFF_IMAG_50\x10\x04\x12\x19\n\x15\x45\x43G_LEAD_OFF_IMAG_100\x10\x05\x12\x19\n\x15\x45\x43G_LEAD_OFF_IMAG_200\x10\x06\x12\x19\n\x15\x45\x43G_LEAD_OFF_IMAG_400\x10\x07*\xc9\x04\n\x1a\x45\x63gLeadOffVoltageThreshold\x12 \n\x1c\x45\x43G_LEAD_OFF_VOL_THRESH_25MV\x10\x00\x12 \n\x1c\x45\x43G_LEAD_OFF_VOL_THRESH_50MV\x10\x01\x12 \n\x1c\x45\x43G_LEAD_OFF_VOL_THRESH_75MV\x10\x02\x12!\n\x1d\x45\x43G_LEAD_OFF_VOL_THRESH_100MV\x10\x03\x12!\n\x1d\x45\x43G_LEAD_OFF_VOL_THRESH_125MV\x10\x04\x12!\n\x1d\x45\x43G_LEAD_OFF_VOL_THRESH_150MV\x10\x05\x12!\n\x1d\x45\x43G_LEAD_OFF_VOL_THRESH_175MV\x10\x06\x12!\n\x1d\x45\x43G_LEAD_OFF_VOL_THRESH_200MV\x10\x07\x12!\n\x1d\x45\x43G_LEAD_OFF_VOL_THRESH_225MV\x10\x08\x12!\n\x1d\x45\x43G_LEAD_OFF_VOL_THRESH_250MV\x10\t\x12!\n\x1d\x45\x43G_LEAD_OFF_VOL_THRESH_275MV\x10\n\x12!\n\x1d\x45\x43G_LEAD_OFF_VOL_THRESH_300MV\x10\x0b\x12!\n\x1d\x45\x43G_LEAD_OFF_VOL_THRESH_325MV\x10\x0c\x12!\n\x1d\x45\x43G_LEAD_OFF_VOL_THRESH_350MV\x10\r\x12!\n\x1d\x45\x43G_LEAD_OFF_VOL_THRESH_375MV\x10\x0e\x12!\n\x1d\x45\x43G_LEAD_OFF_VOL_THRESH_400MV\x10\x0f*\xfe\x01\n\x0e\x45\x63gLeadOffFreq\x12\x1d\n\x19\x45\x43G_LEAD_OFF_FREQ_DISABLE\x10\x00\x12\x1c\n\x18\x45\x43G_LEAD_OFF_FREQ_8192HZ\x10\x01\x12\x1c\n\x18\x45\x43G_LEAD_OFF_FREQ_4096HZ\x10\x02\x12\x1c\n\x18\x45\x43G_LEAD_OFF_FREQ_2048HZ\x10\x03\x12\x1c\n\x18\x45\x43G_LEAD_OFF_FREQ_1024HZ\x10\x04\x12\x1b\n\x17\x45\x43G_LEAD_OFF_FREQ_512HZ\x10\x05\x12\x1b\n\x17\x45\x43G_LEAD_OFF_FREQ_256HZ\x10\x06\x12\x1b\n\x17\x45\x43G_LEAD_OFF_FREQ_128HZ\x10\x07*_\n\rPpgSampleRate\x12\x18\n\x14PPG_SAMPLE_RATE_64HZ\x10\x00\x12\x19\n\x15PPG_SAMPLE_RATE_128HZ\x10\x01\x12\x19\n\x15PPG_SAMPLE_RATE_256HZ\x10\x02*\x96\x01\n\x0f\x41\x63\x63\x65lSampleRate\x12\x19\n\x15\x41\x43\x43_SAMPLE_RATE_12Hz5\x10\x01\x12\x18\n\x14\x41\x43\x43_SAMPLE_RATE_26Hz\x10\x02\x12\x18\n\x14\x41\x43\x43_SAMPLE_RATE_52Hz\x10\x03\x12\x19\n\x15\x41\x43\x43_SAMPLE_RATE_104Hz\x10\x04\x12\x19\n\x15\x41\x43\x43_SAMPLE_RATE_208Hz\x10\x05*i\n\x0e\x41\x63\x63\x65lFullScale\x12\x14\n\x10\x41\x43\x43_FULLSCALE_2g\x10\x00\x12\x15\n\x11\x41\x43\x43_FULLSCALE_16g\x10\x01\x12\x14\n\x10\x41\x43\x43_FULLSCALE_4g\x10\x02\x12\x14\n\x10\x41\x43\x43_FULLSCALE_8g\x10\x03*@\n\nPpgLedType\x12\x0e\n\nPPG_LED_IR\x10\x00\x12\x0f\n\x0bPPG_LED_RED\x10\x01\x12\x11\n\rPPG_LED_GREEN\x10\x02')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'brp_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_SPO2HRDATA'].fields_by_name['spo2']._loaded_options = None
  _globals['_SPO2HRDATA'].fields_by_name['spo2']._serialized_options = b'\020\001'
  _globals['_SPO2HRDATA'].fields_by_name['hr']._loaded_options = None
  _globals['_SPO2HRDATA'].fields_by_name['hr']._serialized_options = b'\020\001'
  _globals['_PACKETTYPE']._serialized_start=6817
  _globals['_PACKETTYPE']._serialized_end=6960
  _globals['_SENSORTYPE']._serialized_start=6962
  _globals['_SENSORTYPE']._serialized_end=7061
  _globals['_COMMANDID']._serialized_start=7064
  _globals['_COMMANDID']._serialized_end=8359
  _globals['_RESPONSECODE']._serialized_start=8362
  _globals['_RESPONSECODE']._serialized_end=8567
  _globals['_NOTIFICATIONID']._serialized_start=8570
  _globals['_NOTIFICATIONID']._serialized_end=8761
  _globals['_ACKRESPONSECODE']._serialized_start=8764
  _globals['_ACKRESPONSECODE']._serialized_end=8999
  _globals['_APPTYPE']._serialized_start=9001
  _globals['_APPTYPE']._serialized_end=9061
  _globals['_SENSORMODE']._serialized_start=9063
  _globals['_SENSORMODE']._serialized_end=9172
  _globals['_LOGLEVEL']._serialized_start=9174
  _globals['_LOGLEVEL']._serialized_end=9269
  _globals['_CHARGINGSTATUS']._serialized_start=9271
  _globals['_CHARGINGSTATUS']._serialized_end=9350
  _globals['_CHARGINGERROR']._serialized_start=9353
  _globals['_CHARGINGERROR']._serialized_end=9607
  _globals['_BLETXPOWERLEVEL']._serialized_start=9610
  _globals['_BLETXPOWERLEVEL']._serialized_end=9838
  _globals['_ECGSAMPLERATE']._serialized_start=9840
  _globals['_ECGSAMPLERATE']._serialized_end=9935
  _globals['_ECGPGAGAIN']._serialized_start=9937
  _globals['_ECGPGAGAIN']._serialized_end=10050
  _globals['_ECGINAGAIN']._serialized_start=10052
  _globals['_ECGINAGAIN']._serialized_end=10144
  _globals['_ECGINARANGE']._serialized_start=10146
  _globals['_ECGINARANGE']._serialized_end=10255
  _globals['_ECGINPUTPOLARITY']._serialized_start=10257
  _globals['_ECGINPUTPOLARITY']._serialized_end=10327
  _globals['_ECGLEADOFFMODE']._serialized_start=10329
  _globals['_ECGLEADOFFMODE']._serialized_end=10387
  _globals['_ECGLEADOFFCURRENTPOLARITY']._serialized_start=10389
  _globals['_ECGLEADOFFCURRENTPOLARITY']._serialized_end=10474
  _globals['_ECGLEADOFFCURRENTMAGNITUDE']._serialized_start=10477
  _globals['_ECGLEADOFFCURRENTMAGNITUDE']._serialized_end=10714
  _globals['_ECGLEADOFFVOLTAGETHRESHOLD']._serialized_start=10717
  _globals['_ECGLEADOFFVOLTAGETHRESHOLD']._serialized_end=11302
  _globals['_ECGLEADOFFFREQ']._serialized_start=11305
  _globals['_ECGLEADOFFFREQ']._serialized_end=11559
  _globals['_PPGSAMPLERATE']._serialized_start=11561
  _globals['_PPGSAMPLERATE']._serialized_end=11656
  _globals['_ACCELSAMPLERATE']._serialized_start=11659
  _globals['_ACCELSAMPLERATE']._serialized_end=11809
  _globals['_ACCELFULLSCALE']._serialized_start=11811
  _globals['_ACCELFULLSCALE']._serialized_end=11916
  _globals['_PPGLEDTYPE']._serialized_start=11918
  _globals['_PPGLEDTYPE']._serialized_end=11982
  _globals['_PROTOCOLINFO']._serialized_start=18
  _globals['_PROTOCOLINFO']._serialized_end=63
  _globals['_PACKET']._serialized_start=66
  _globals['_PACKET']._serialized_end=289
  _globals['_COMMANDPACKET']._serialized_start=292
  _globals['_COMMANDPACKET']._serialized_end=781
  _globals['_RESPONSEPACKET']._serialized_start=784
  _globals['_RESPONSEPACKET']._serialized_end=1348
  _globals['_NOTIFICATIONPACKET']._serialized_start=1351
  _globals['_NOTIFICATIONPACKET']._serialized_end=1612
  _globals['_ACKPACKET']._serialized_start=1614
  _globals['_ACKPACKET']._serialized_end=1697
  _globals['_DEVINFO']._serialized_start=1700
  _globals['_DEVINFO']._serialized_end=1887
  _globals['_CMDMEMSET']._serialized_start=1889
  _globals['_CMDMEMSET']._serialized_end=1947
  _globals['_CMDMEMGET']._serialized_start=1949
  _globals['_CMDMEMGET']._serialized_end=1993
  _globals['_RSPMEMGET']._serialized_start=1995
  _globals['_RSPMEMGET']._serialized_end=2020
  _globals['_NOTILOG']._serialized_start=2022
  _globals['_NOTILOG']._serialized_end=2045
  _globals['_AFESETTINGS']._serialized_start=2048
  _globals['_AFESETTINGS']._serialized_end=3255
  _globals['_WLCRUNPARAMS']._serialized_start=3258
  _globals['_WLCRUNPARAMS']._serialized_end=3458
  _globals['_WLCOEMPARAMS']._serialized_start=3461
  _globals['_WLCOEMPARAMS']._serialized_end=4437
  _globals['_SENSORCONFIG']._serialized_start=4439
  _globals['_SENSORCONFIG']._serialized_end=4522
  _globals['_SPO2HRDATA']._serialized_start=4524
  _globals['_SPO2HRDATA']._serialized_end=4570
  _globals['_SELFTESTDATA']._serialized_start=4572
  _globals['_SELFTESTDATA']._serialized_end=4681
  _globals['_DEVSTATUS']._serialized_start=4684
  _globals['_DEVSTATUS']._serialized_end=4992
  _globals['_POWERMANAGEMENT']._serialized_start=4994
  _globals['_POWERMANAGEMENT']._serialized_end=5028
  _globals['_SAMPLETHRESHOLD']._serialized_start=5030
  _globals['_SAMPLETHRESHOLD']._serialized_end=5150
  _globals['_BLECONNECTPARAMS']._serialized_start=5152
  _globals['_BLECONNECTPARAMS']._serialized_end=5274
  _globals['_BLESETTINGS']._serialized_start=5277
  _globals['_BLESETTINGS']._serialized_end=5439
  _globals['_LOGSETTINGS']._serialized_start=5441
  _globals['_LOGSETTINGS']._serialized_end=5508
  _globals['_ECGGAIN']._serialized_start=5510
  _globals['_ECGGAIN']._serialized_end=5626
  _globals['_ECGLEADOFFPARAMS']._serialized_start=5629
  _globals['_ECGLEADOFFPARAMS']._serialized_end=5940
  _globals['_ECGSETTINGS']._serialized_start=5943
  _globals['_ECGSETTINGS']._serialized_end=6169
  _globals['_PPGLEDCONTROL']._serialized_start=6171
  _globals['_PPGLEDCONTROL']._serialized_end=6225
  _globals['_PPGLEDSETTINGS']._serialized_start=6227
  _globals['_PPGLEDSETTINGS']._serialized_end=6339
  _globals['_PPGSETTINGS']._serialized_start=6341
  _globals['_PPGSETTINGS']._serialized_end=6462
  _globals['_ACCELSETTINGS']._serialized_start=6464
  _globals['_ACCELSETTINGS']._serialized_end=6591
  _globals['_ALLDEVSETTINGS']._serialized_start=6594
  _globals['_ALLDEVSETTINGS']._serialized_end=6814
# @@protoc_insertion_point(module_scope)
