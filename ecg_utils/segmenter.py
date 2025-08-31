# ecg_utils/segmenter.py

import wfdb
from scipy.signal import resample
import numpy as np

class Segmention:
    """
    Class for preprocessing ECG signals:
    - Resampling to a fixed frequency (default 360Hz)
    - Segmenting into fixed-length windows (default: 10 seconds)
    """

    def __init__(self, fs=360):
        self.fs = fs

    def resample(self, path, signal_name, channel_index):
        """
        Load and resample an ECG signal.
        path: folder path (should end with '/')
        signal_name: name of record (string)
        channel_index: index of channel to load
        """
        record = wfdb.rdrecord(path + signal_name)
        signal = record.p_signal[:, channel_index]
        original_fs = record.fs
        duration = len(signal) / original_fs
        new_length = int(duration * self.fs)
        
        resampled_signal = resample(signal, new_length)
        return resampled_signal

    def segment(self, path, signal_name, channel_index, duration_minutes=2):
        """
        Segment ECG into 10-second windows, with configurable duration.
        duration_minutes: number of minutes to cut from the start of the record
        Returns list of segments (each of length fs*10). If last window incomplete -> discarded.
        """
        full_signal = self.resample(path, signal_name, channel_index)
        
        max_samples = int(self.fs * 60 * duration_minutes)
        
        samples_to_use = max_samples

        full_signal = full_signal[:samples_to_use]
        seg_signal = []
        window_size = self.fs * 10  # 10 seconds

        num_segments = samples_to_use // window_size
        for i in range(int(num_segments)):
            start = int(i * window_size)
            end = int(start + window_size)
            seg_signal.append(full_signal[start:end])

        return seg_signal
