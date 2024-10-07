import proto.brp_pb2 as brp
from core.enum.accel_full_scale_range import AccelFullScaleRange
from core.enum.accel_sampling_rate import AccelSamplingRate
from core.enum.app_type import AppType
from core.enum.charging_error import ChargingError
from core.enum.charging_status import ChargingStatus
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


class ProtobufUtils:

    @staticmethod
    def to_app_type(brp_app_type: brp.AppType) -> AppType:
        mapping = {
            brp.AppType.APP_TYPE_BOOT_LOADER: AppType.BOOT_LOADER,
            brp.AppType.APP_TYPE_APPLICATION: AppType.APPLICATION,
        }
        return mapping.get(brp_app_type, None)

    @staticmethod
    def to_charging_status(brp_charging_status: brp.ChargingStatus) -> ChargingStatus:
        mapping = {
            brp.ChargingStatus.CHARGING_STATUS_DISCHARGING: ChargingStatus.DISCHARGING,
            brp.ChargingStatus.CHARGING_STATUS_CHARGING: ChargingStatus.CHARGING,
        }
        return mapping.get(brp_charging_status, None)

    @staticmethod
    def to_charging_error(brp_charging_error: brp.ChargingError) -> ChargingError:
        mapping = {
            brp.ChargingError.CHARGING_ERROR_OK: ChargingError.OK,
            brp.ChargingError.CHARGING_ERROR_IC_TEMP: ChargingError.IC_TEMP,
            brp.ChargingError.CHARGING_ERROR_PROTOCOL: ChargingError.PROTOCOL,
            brp.ChargingError.CHARGING_ERROR_BATT_CONNECT: ChargingError.BATT_CONNECT,
            brp.ChargingError.CHARGING_ERROR_BATT_TEMP: ChargingError.BATT_TEMP,
            brp.ChargingError.CHARGING_ERROR_TCM_TIMEOUT: ChargingError.TCM_TIMEOUT,
            brp.ChargingError.CHARGING_ERROR_CCM_TIMEOUT: ChargingError.CCM_TIMEOUT,
            brp.ChargingError.CHARGING_ERROR_CVM_TIMEOUT: ChargingError.CVM_TIMEOUT,

        }
        return mapping.get(brp_charging_error, None)

    @staticmethod
    def to_ecg_lead_off_mode(brp_ecg_lead_off_mode: brp.EcgLeadOffMode) -> EcgLeadOffMode:
        mapping = {
            brp.EcgLeadOffMode.ECG_LEAD_OFF_DC: EcgLeadOffMode.ECG_LEAD_OFF_DC,
            brp.EcgLeadOffMode.ECG_LEAD_OFF_AC: EcgLeadOffMode.ECG_LEAD_OFF_AC,
        }
        return mapping.get(brp_ecg_lead_off_mode, None)

    @staticmethod
    def to_ecg_lead_off_current_polarity(
            brp_ecg_lead_off_current_polarity: brp.EcgLeadOffCurrentPolarity) -> EcgLeadOffCurrentPolarity:
        mapping = {
            brp.EcgLeadOffCurrentPolarity.ECG_LEAD_OFF_NON_INVERTED: EcgLeadOffCurrentPolarity.ECG_LEAD_OFF_NON_INVERTED,
            brp.EcgLeadOffCurrentPolarity.ECG_LEAD_OFF_INVERTED: EcgLeadOffCurrentPolarity.ECG_LEAD_OFF_INVERTED,
        }
        return mapping.get(brp_ecg_lead_off_current_polarity, None)

    @staticmethod
    def to_ecg_lead_off_current_magnitude(
            brp_ecg_lead_off_current_magnitude: brp.EcgLeadOffCurrentMagnitude) -> EcgLeadOffCurrentMagnitude:
        mapping = {
            brp.EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_0: EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_0,
            brp.EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_5: EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_5,
            brp.EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_10: EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_10,
            brp.EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_20: EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_20,
            brp.EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_50: EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_50,
            brp.EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_100: EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_100,
            brp.EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_200: EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_200,
            brp.EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_400: EcgLeadOffCurrentMagnitude.ECG_LEAD_OFF_IMAG_400,
        }
        return mapping.get(brp_ecg_lead_off_current_magnitude, None)

    @staticmethod
    def to_ecg_lead_off_voltage_threshold(
            brp_ecg_lead_off_voltage_threshold: brp.EcgLeadOffVoltageThreshold) -> EcgLeadOffVoltageThreshold:
        mapping = {
            brp.EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_25MV: EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_25MV,
            brp.EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_50MV: EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_50MV,
            brp.EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_75MV: EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_75MV,
            brp.EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_100MV: EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_100MV,
            brp.EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_125MV: EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_125MV,
            brp.EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_150MV: EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_150MV,
            brp.EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_175MV: EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_175MV,
            brp.EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_200MV: EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_200MV,
            brp.EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_225MV: EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_225MV,
            brp.EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_250MV: EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_250MV,
            brp.EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_275MV: EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_275MV,
            brp.EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_300MV: EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_300MV,
            brp.EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_325MV: EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_325MV,
            brp.EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_350MV: EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_350MV,
            brp.EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_375MV: EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_375MV,
            brp.EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_400MV: EcgLeadOffVoltageThreshold.ECG_LEAD_OFF_VOL_THRESH_400MV,

        }
        return mapping.get(brp_ecg_lead_off_voltage_threshold, None)

    @staticmethod
    def to_ecg_lead_off_freq(brp_ecg_lead_off_freq: brp.EcgLeadOffFreq) -> EcgLeadOffFreq:
        mapping = {
            brp.EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_DISABLE: EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_DISABLE,
            brp.EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_8192HZ: EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_8192HZ,
            brp.EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_4096HZ: EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_4096HZ,
            brp.EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_2048HZ: EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_2048HZ,
            brp.EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_1024HZ: EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_1024HZ,
            brp.EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_512HZ: EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_512HZ,
            brp.EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_256HZ: EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_256HZ,
            brp.EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_128HZ: EcgLeadOffFreq.ECG_LEAD_OFF_FREQ_128HZ,
        }
        return mapping.get(brp_ecg_lead_off_freq, None)

    @staticmethod
    def to_ecg_sampling_rate(brp_ecg_sampling_rate: brp.EcgSampleRate) -> EcgSamplingRate:
        mapping = {
            brp.EcgSampleRate.ECG_SAMPLE_RATE_64HZ: EcgSamplingRate.ECG_SAMPLE_RATE_64HZ,
            brp.EcgSampleRate.ECG_SAMPLE_RATE_128HZ: EcgSamplingRate.ECG_SAMPLE_RATE_128HZ,
            brp.EcgSampleRate.ECG_SAMPLE_RATE_256HZ: EcgSamplingRate.ECG_SAMPLE_RATE_256HZ,
        }
        return mapping.get(brp_ecg_sampling_rate, None)

    @staticmethod
    def to_ecg_pga_gain(brp_ecg_pga_gain: brp.EcgPgaGain) -> EcgPgaGain:
        mapping = {
            brp.EcgPgaGain.ECG_PGA_GAIN_1: EcgPgaGain.PGA_GAIN_1,
            brp.EcgPgaGain.ECG_PGA_GAIN_2: EcgPgaGain.PGA_GAIN_2,
            brp.EcgPgaGain.ECG_PGA_GAIN_4: EcgPgaGain.PGA_GAIN_4,
            brp.EcgPgaGain.ECG_PGA_GAIN_8: EcgPgaGain.PGA_GAIN_8,
            brp.EcgPgaGain.ECG_PGA_GAIN_16: EcgPgaGain.PGA_GAIN_16,
        }
        return mapping.get(brp_ecg_pga_gain, None)

    @staticmethod
    def to_ecg_ina_gain(brp_ecg_ina_gain: brp.EcgInaGain) -> EcgInaGain:
        mapping = {
            brp.EcgInaGain.ECG_INA_GAIN_0: EcgInaGain.INA_GAIN_0,
            brp.EcgInaGain.ECG_INA_GAIN_1: EcgInaGain.INA_GAIN_1,
            brp.EcgInaGain.ECG_INA_GAIN_2: EcgInaGain.INA_GAIN_2,
            brp.EcgInaGain.ECG_INA_GAIN_3: EcgInaGain.INA_GAIN_3,

        }
        return mapping.get(brp_ecg_ina_gain, None)

    @staticmethod
    def to_ecg_ina_range(brp_ecg_ina_range: brp.EcgInaRange) -> EcgInaRange:
        mapping = {
            brp.EcgInaRange.ECG_INA_GAIN_RGE_0: EcgInaRange.ECG_INA_GAIN_RGE_0,
            brp.EcgInaRange.ECG_INA_GAIN_RGE_1: EcgInaRange.ECG_INA_GAIN_RGE_1,
            brp.EcgInaRange.ECG_INA_GAIN_RGE_2: EcgInaRange.ECG_INA_GAIN_RGE_2,
            brp.EcgInaRange.ECG_INA_GAIN_RGE_3: EcgInaRange.ECG_INA_GAIN_RGE_3,
        }
        return mapping.get(brp_ecg_ina_range, None)

    @staticmethod
    def to_ecg_input_polarity(brp_ecg_input_polarity: brp.EcgInputPolarity) -> EcgInputPolarity:
        mapping = {
            brp.EcgInputPolarity.ECG_INPUT_NON_INVERTED: EcgInputPolarity.ECG_INPUT_NON_INVERTED,
            brp.EcgInputPolarity.ECG_INPUT_INVERTED: EcgInputPolarity.ECG_INPUT_INVERTED,
        }
        return mapping.get(brp_ecg_input_polarity, None)

    @staticmethod
    def to_ppg_sample_rate(brp_ppg_sample_rate: brp.PpgSampleRate) -> PpgSamplingRate:
        mapping = {
            brp.PpgSampleRate.PPG_SAMPLE_RATE_64HZ: PpgSamplingRate.ECG_SAMPLE_RATE_64HZ,
            brp.PpgSampleRate.PPG_SAMPLE_RATE_128HZ: PpgSamplingRate.ECG_SAMPLE_RATE_128HZ,
            brp.PpgSampleRate.PPG_SAMPLE_RATE_256HZ: PpgSamplingRate.ECG_SAMPLE_RATE_256HZ,

        }
        return mapping.get(brp_ppg_sample_rate, None)

    @staticmethod
    def to_accel_sampling_rate(brp_accel_sample_rate: brp.AccelSampleRate) -> AccelSamplingRate:
        mapping = {
            brp.AccelSampleRate.ACC_SAMPLE_RATE_12Hz5: AccelSamplingRate.ACC_SAMPLE_RATE_12Hz5,
            brp.AccelSampleRate.ACC_SAMPLE_RATE_26Hz: AccelSamplingRate.ACC_SAMPLE_RATE_26Hz,
            brp.AccelSampleRate.ACC_SAMPLE_RATE_52Hz: AccelSamplingRate.ACC_SAMPLE_RATE_52Hz,
        }
        return mapping.get(brp_accel_sample_rate, None)

    @staticmethod
    def to_accel_full_scale_range(brp_accel_full_scale_range: brp.AccelFullScale) -> AccelFullScaleRange:
        mapping = {
            brp.AccelFullScale.ACC_FULLSCALE_2g: AccelFullScaleRange.ACC_FS_2G,
            brp.AccelFullScale.ACC_FULLSCALE_16g: AccelFullScaleRange.ACC_FS_16G,
            brp.AccelFullScale.ACC_FULLSCALE_4g: AccelFullScaleRange.ACC_FS_4G,
            brp.AccelFullScale.ACC_FULLSCALE_8g: AccelFullScaleRange.ACC_FS_8G,
        }
        return mapping.get(brp_accel_full_scale_range, None)

    @staticmethod
    def to_power_level(brp_power_level: brp.BleTxPowerLevel) -> PowerLevel:
        mapping = {
            brp.BleTxPowerLevel.BLE_TX_POWER_LEVEL_NEG_20: PowerLevel.NEG_20,
            brp.BleTxPowerLevel.BLE_TX_POWER_LEVEL_NEG_16: PowerLevel.NEG_16,
            brp.BleTxPowerLevel.BLE_TX_POWER_LEVEL_NEG_12: PowerLevel.NEG_12,
            brp.BleTxPowerLevel.BLE_TX_POWER_LEVEL_NEG_6: PowerLevel.NEG_6,
            brp.BleTxPowerLevel.BLE_TX_POWER_LEVEL_0: PowerLevel.POS_0,
            brp.BleTxPowerLevel.BLE_TX_POWER_LEVEL_4: PowerLevel.POS_4,
        }
        return mapping.get(brp_power_level, None)

    @staticmethod
    def to_log_level(brp_log_level: brp.LogLevel) -> LogLevel:
        mapping = {
            brp.LogLevel.LOG_LEVEL_ERROR: LogLevel.ERROR,
            brp.LogLevel.LOG_LEVEL_WARNING: LogLevel.WARNING,
            brp.LogLevel.LOG_LEVEL_INFO: LogLevel.INFO,
            brp.LogLevel.LOG_LEVEL_DEBUG: LogLevel.DEBUG,
        }
        return mapping.get(brp_log_level, None)
