# ecg_utils/dataset_builder.py

import pandas as pd
from ecg_utils.segmenter import Segmention
from ecg_utils.feature_extractor import FeatureExtractor

def data_set(path, signal_names, channel_index, label, output_csv, fs=360, duration_minutes=2):
    """
    Build dataset of ECG features per 10s window from multiple signals.
    duration_minutes: how many minutes to cut from each record (default 2)
    """
    segmenter = Segmention(fs=fs)
    extractor = FeatureExtractor(fs=fs)

    all_features = []

    for sig in signal_names:
        try:
            segments = segmenter.segment(path, sig, channel_index, duration_minutes=duration_minutes)
            
            for window in segments:
                features = extractor.compute_features(window)
                # features is a DataFrame with one row
                features["label"] = label
                all_features.append(features)
        except Exception as e:
            print(f"Error with {sig}: {e}")

    if all_features:
        df = pd.concat(all_features, ignore_index=True)
        df.to_csv(output_csv, index=False)
        print(f"Saved dataset to {output_csv} (n_samples={len(df)})")
    else:
        print("No features extracted.")
