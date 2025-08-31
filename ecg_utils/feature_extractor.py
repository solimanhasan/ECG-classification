# ecg_utils/feature_extractor.py

import numpy as np
import pandas as pd
import neurokit2 as nk
from scipy.signal import butter, filtfilt, find_peaks

class FeatureExtractor:
    """
    Class for extracting ECG features from a given signal.
    Applies filtering, R-peak detection, waveform delineation,
    and computes temporal, statistical, and morphological features.
    """

    def __init__(self, fs=360):
        self.fs = fs

    def bandpass_filter(self, signal, lowcut=0.5, highcut=40.0):
        """
        Apply Butterworth bandpass filter to remove noise.

        Parameters:
        signal (np.array): Raw ECG signal
        lowcut (float): Low cutoff frequency
        highcut (float): High cutoff frequency

        Returns:
        filtered (np.array): Filtered signal
        """
        nyq = 0.5 * self.fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(1, [low, high], btype='band')
        return filtfilt(b, a, signal)

    def detect_r_peaks(self, signal):
        """
        Detect R-peaks using a simplified Pan-Tompkins approach.

        Parameters:
        signal (np.array): Filtered ECG signal

        Returns:
        r_peaks (np.array): Indices of R-peaks
        """
        filtered = self.bandpass_filter(signal)
        diff = np.diff(filtered, prepend=filtered[0])
        squared = diff ** 2
        integrated = np.convolve(squared, np.ones(40)/40, mode='same')
        threshold = np.mean(integrated) * 1.2
        r_peaks, _ = find_peaks(integrated, height=threshold, distance=int(0.25 * self.fs))
        return r_peaks

    def compute_features(self, signal):
        """
        Extract ECG features from a signal segment.

        Parameters:
        signal (np.array): Segment of ECG signal

        Returns:
        features_df (pd.DataFrame): Single-row dataframe of features
        """
        r_peaks = self.detect_r_peaks(signal)
        rr = np.diff(r_peaks) / self.fs
        hr = 60 / rr 
        rmssd = np.sqrt(np.mean(np.square(np.diff(rr)))) 

        delineate = nk.ecg_delineate(signal, rpeaks={"ECG_R_Peaks": r_peaks}, sampling_rate=self.fs, method="dwt")[1]
        q_peaks = np.array(delineate["ECG_Q_Peaks"])
        s_peaks = np.array(delineate["ECG_S_Peaks"])
        t_peaks = np.array(delineate["ECG_T_Peaks"])

        q_peaks = q_peaks[~np.isnan(q_peaks)].astype(int)
        s_peaks = s_peaks[~np.isnan(s_peaks)].astype(int)
        t_peaks = t_peaks[~np.isnan(t_peaks)].astype(int)

        min_len = min(len(q_peaks), len(s_peaks), len(t_peaks))

        qrs_durations = (s_peaks[:min_len] - q_peaks[:min_len]) / self.fs * 1000
        qt_intervals = (t_peaks[:min_len] - q_peaks[:min_len]) / self.fs * 1000
        st_amplitudes = signal[t_peaks[:min_len]] - signal[s_peaks[:min_len]]
        st_slopes = st_amplitudes / ((t_peaks[:min_len] - s_peaks[:min_len]) / self.fs)
        st_max = np.max(st_amplitudes)
        st_min = np.min(st_amplitudes) 

        features = {
            "RR_mean": np.mean(rr) ,
            "RR_std": np.std(rr) ,
            "HR_mean": np.mean(hr),
            "HR_std": np.std(hr),
            "RMSSD": rmssd,
            "QRS_mean": np.mean(qrs_durations),
            "QT_mean": np.mean(qt_intervals) ,
            "ST_amp_mean": np.mean(st_amplitudes) ,
            "ST_slope_mean": np.mean(st_slopes),
            "ST_amp_max": st_max,
            "ST_amp_min": st_min
        }

        return pd.DataFrame([features])