import numpy as np
import scipy.signal
from scipy.signal import find_peaks
from scipy.fft import fft, fftfreq
from utils import butter_bandpass_filter, butter_lowpass_filter
from define import NUM_CH, PPG_GAIN, CHANNELS_COLOR, CHANNELS_LABEL, SAMPLE_TIME_1S_RAW_DATA, SAMPLE_TIME_1S_PPG_DATA, \
    PORT, BAUD_RATE, FS_128, DIR_SAVE, SUBJECT_ID, FS_DEVICE, THR_KURTOSIS, THR_STD

N_SAMPLES = 128*4

def compute_spo2(ppg_red, ppg_ir):
    # Compute the AC component for both PPG signals
    ac_red = ppg_red - np.mean(ppg_red)
    ac_ir = ppg_ir - np.mean(ppg_ir)

    # Find peaks in the AC components
    peaks_red, _ = find_peaks(ac_red, height=0)
    peaks_ir, _ = find_peaks(ac_ir, height=0)

    # Compute the mean peak-to-peak amplitude for both PPG signals
    amp_red = np.mean(ac_red[peaks_red])
    amp_ir = np.mean(ac_ir[peaks_ir])

    # Calculate the R value
    r = amp_red / amp_ir

    # Calculate SPO2 using the R value
    spo2 = 110 - 25 * r
    # print('--------- SpO2: {} r: {} '.format(spo2, -16.666666*r*r + 8.333333*r + 101))
    spo2 = int(round(spo2))
    if spo2 > 100:
        spo2 = 100

    return spo2

def compute_fft(signal, fs=FS_DEVICE):
    x = fft(signal)
    f_resolution = fs / len(signal)
    X_magnitude = np.abs(x)[:len(signal) // 2]
    _x = f_resolution * np.arange(len(x) // 2)

    return _x, X_magnitude

def compute_hr_spo2(ppg_red, ppg_ir):
    ppg_lp_ppg_red = butter_lowpass_filter(ppg_red, 5, FS_DEVICE, 2)
    ppg_fil_ppg_red = butter_bandpass_filter(ppg_red, 0.5, 5, FS_DEVICE, 2)
    ppg_lp_ppg_ir = butter_lowpass_filter(ppg_ir, 5, FS_DEVICE, 2)
    ppg_fil_ppg_ir = butter_bandpass_filter(ppg_ir, 0.5, 5, FS_DEVICE, 2)

    ac_red = ppg_fil_ppg_red[-N_SAMPLES:]
    dc_red = ppg_lp_ppg_red[-N_SAMPLES:]
    ac_ir = ppg_fil_ppg_ir[-N_SAMPLES:]
    dc_ir = ppg_lp_ppg_ir[-N_SAMPLES:]

    ppg_ai = np.asarray([ac_red, ac_ir])
    std = np.std(ppg_ai, axis=1)
    kurtosis = np.mean(np.power(ppg_ai-np.mean(ppg_ai, axis=1)[:, None], 4), axis=1) / np.power(np.std(ppg_ai, axis=1), 4)

    # print('********** SQI Kurt: {} std: {}'.format(kurtosis, std))

    if (kurtosis[1] > THR_KURTOSIS):
        return -1, -1
    peaks_ecg = scipy.signal.find_peaks(ppg_red)[0]
    
    # Calculate Peak2Peak interval
    peak_times = peaks_ecg / FS_DEVICE
    inter_peak_intervals = np.diff(peak_times)\

    # Calculate Heart Rate using the Peak2Peak interval
    hr = 60 / np.mean(inter_peak_intervals)

    # hr = 60 * FS_DEVICE / np.mean(np.diff(peaks_ecg))
    hr = int(round(hr))
    ind = np.where(((kurtosis < 1.78) | (kurtosis > THR_KURTOSIS+0.12)))[0]
    if len(ind) != 0:
        return hr, -1

    ac_red = np.sqrt(np.mean(np.square(ppg_fil_ppg_red[-N_SAMPLES:] - ppg_lp_ppg_red[-N_SAMPLES:])))
    dc_red = np.mean(ppg_lp_ppg_red[-N_SAMPLES:])

    ac_ir = np.sqrt(np.mean(np.square(ppg_fil_ppg_ir[-N_SAMPLES:] - ppg_lp_ppg_ir[-N_SAMPLES:])))
    dc_ir = np.mean(ppg_lp_ppg_ir[-N_SAMPLES:])

    r = (ac_red / dc_red) / (ac_ir / dc_ir)

    spo2 = 110 - 25 * r
    # spo2 = -16.666666*r*r + 8.333333*r + 101
    # print('--------- SpO2: {} r: {}  kurtosis: {}'.format(spo2, -16.666666*r*r + 8.333333*r + 101, kurtosis[1]))

    spo2 = int(round(spo2))
    if spo2 > 100:
        spo2 = 100
    return hr, spo2

def moving_average(data, window_size):
    """
    Tính toán giá trị trung bình động của dữ liệu.

    Parameters:
        data (numpy.array): input data (1D array).
        window_size (int): sliding window size.

    Returns:
        numpy.array: filtered data.
    """
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

def baseline_filter(ecg_data, window_size=100):
    """
    Filter baseline of ECG data using a moving average filter.

    Parameters:
        ecg_data (numpy.array): input ECG data (1D array).
        window_size (int): sliding window size for the moving average filter.

    Returns:
        numpy.array: baseline-filtered ECG data.
    """
    return ecg_data - moving_average(ecg_data, window_size)

def detect_peak_ecg(ecg):
    ecg_signal = np.array(ecg)
    peaks_ecg, _ = scipy.signal.find_peaks(ecg_signal, threshold=(-2000, 2000), height=700, distance=50)

    return peaks_ecg, ecg_signal[peaks_ecg]

def detect_peak_ppg(ppg):
    ppg_signal = np.array(ppg)
    peaks_ppg, _ = scipy.signal.find_peaks(ppg_signal, threshold=(-200, 200), height=10, distance=50)

    return peaks_ppg, ppg_signal[peaks_ppg]

def calculate_hr(ppg_peaks, sampling_rate):
    hr = []
    hr_avg = 0
    if len(ppg_peaks) > 3:
        peak_times = ppg_peaks / sampling_rate
        inter_peak_intervals = np.diff(peak_times)
        # Calculate Heart Rate from time intervals
        hr = 60 / inter_peak_intervals
        # print(hr)
        values = [value for value in hr if value is not None]
        hr_avg = sum(values) / len(values)
        for i in range(len(hr)-1):
            if abs(hr[i] - hr[i+1]) > 10:
                hr_avg = 0
    return round(hr_avg)

def calculate_ptt(ecg_peaks, ppg_peaks, sampling_rate):
    ptt = []
    ptt_n = 0
    if len(ppg_peaks) > 3:
        if len(ecg_peaks) == len(ppg_peaks):
            for i in range(len(ecg_peaks) - 1):
                ecg_peak = ecg_peaks[i]
                ppg_peak = ppg_peaks[i]
                time_diff = (abs(ppg_peak - ecg_peak) / sampling_rate) * 1000
                ptt.append(time_diff)
                ptt_n = ptt_n + 1
    if ptt_n > 0:
        for i in range(ptt_n - 1):
            if abs(ptt[i] - ptt[i+1]) > 100:
                ptt_n = 0
            if ptt[i] > 400:
                ptt_n = 0
    return ptt_n, ptt

def create_a_signed_number(number, bit):
    # Maximum positive value for a signed number
    max_value = (1 << (bit - 1)) - 1

    # Minimum negative value for an signed number
    _min_value = -(1 << (bit - 1))

    # Converting it to a decimal value
    decimal_value = number if number <= max_value else number - (1 << bit)
    return decimal_value
