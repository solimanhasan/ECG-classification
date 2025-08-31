# CODEBOOK — ECG Feature Definitions

This codebook documents the features extracted from each 10-second ECG segment by `FeatureExtractor` (see `ecg_utils/feature_extractor.py`).

Each feature is computed per window and saved in the per-class CSVs (`normal.csv`, `afib.csv`, `mi.csv`), then merged into `final_dataset.csv`.

---

## 1. Temporal & Heart Rate Variability (HRV) Features

- **RR_mean**  
  Mean of RR intervals (time between successive R-peaks).  
  Units: seconds  
  Interpretation: average heartbeat interval.

- **RR_std**  
  Standard deviation of RR intervals.  
  Units: seconds  
  Interpretation: variability of heart rhythm; higher in arrhythmias.

- **HR_mean**  
  Mean heart rate over the window.  
  Units: beats per minute (bpm)  
  Interpretation: overall heart rate.

- **HR_std**  
  Standard deviation of instantaneous heart rate.  
  Units: bpm  
  Interpretation: beat-to-beat heart rate variability.

- **RMSSD**  
  Root Mean Square of Successive Differences between RR intervals.  
  Units: seconds  
  Interpretation: common HRV metric, sensitive to parasympathetic activity.

---

## 2. Morphological Features

- **QRS_mean**  
  Mean QRS duration = (S_peak − Q_peak).  
  Units: milliseconds (ms)  
  Interpretation: ventricular depolarization duration; prolonged in bundle branch block or conduction defects.

- **QT_mean**  
  Mean QT interval = (T_peak − Q_peak).  
  Units: ms  
  Interpretation: ventricular depolarization + repolarization; prolonged QT may indicate risk of arrhythmia.

---

## 3. ST Segment Features

- **ST_amp_mean**  
  Mean ST amplitude = (T_peak amplitude − S_peak amplitude).  
  Units: arbitrary units (depends on ECG scaling, usually mV).  
  Interpretation: average deviation of ST segment; elevated/depressed ST suggests ischemia or infarction.

- **ST_slope_mean**  
  Mean slope of ST segment = ΔAmplitude / ΔTime (T − S).  
  Units: mV/s  
  Interpretation: slope abnormality is a potential ischemia marker.

- **ST_amp_max**  
  Maximum ST amplitude among windows.  
  Units: mV  
  Interpretation: most pronounced ST elevation.

- **ST_amp_min**  
  Minimum ST amplitude among windows.  
  Units: mV  
  Interpretation: most pronounced ST depression.

---

## Notes
- Features are derived from R/Q/S/T peaks as detected by `neurokit2.ecg_delineate` (wavelet method).
- Units may vary depending on ECG dataset scaling; interpret relative differences across classes.
- Missing values (NaN) may occur if peaks cannot be detected in a given segment — these rows should be cleaned before training.

---

## Labels
- **label = 0** → Normal  
- **label = 1** → AFib  
- **label = 2** → MI
