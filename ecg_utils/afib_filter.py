# ecg_utils/afib_filter.py

import pandas as pd

class AfibCleaner:
    def __init__(self, reference_csv="normal.csv", features=["RR_std", "RMSSD", "HR_std"]):
        """
        reference_csv: path to CSV of normal windows to compute thresholds
        features: list of feature names to use for filtering
        
        """
        
        df_ref = pd.read_csv(reference_csv)
        self.features = features
        self.thresholds = {}
        for f in features:
            
            mu = df_ref[f].mean()
            sigma = df_ref[f].std()
            self.thresholds[f] = (mu, sigma)

    def get_thresholds(self):
        # return thresholds as dict {feature: numeric_threshold}
        return {f: self.thresholds[f][0] for f in self.features}

    def clean(self, afib_csv, output_csv="afib_clean.csv"):
        
        df_afib = pd.read_csv(afib_csv)
        thr = self.get_thresholds()

        
        for f in self.features:
            cond =  (df_afib[f] > thr[f])

        df_filtered = df_afib[cond]
        df_filtered.to_csv(output_csv, index=False)
        print(f"Saved cleaned AFib dataset to {output_csv} (original={len(df_afib)}, kept={len(df_filtered)})")
        return df_filtered
