# ECG Classification (Normal / AFib / MI) — Reproducible Pipeline

**English README**

## Overview 
This repository contains a reproducible pipeline for ECG classification using handcrafted features (time-domain, statistical, morphological) and classic ML models: **Normal**, **Atrial Fibrillation (AFib)**, و **Myocardial Infarction (MI)**

- Signal preprocessing: resampling → segmentation (10s windows, duration configurable).
- Feature extraction: R-peak detection, RR metrics (mean/std/RMSSD), QRS/QT, ST measures.
- Models: Decision Tree (baseline) with planned comparisons (RF, SVM, KNN, MLP).
- Reproducibility: exact record lists + public data links (no raw signals committed).

## Data Sources & Records 
We **do not** commit raw WFDB signals due to size & licensing. :

### 1) Normal — MIT‑BIH Normal Sinus Rhythm Database (NSRDB)
PhysioNet page: https://physionet.org/content/nsrdb/1.0.0/
**Records used:** `16265, 16272, 16273, 16420, 16483, 16539, 16773, 16786, 16795, 17052`

### 2) AFib — MIT‑BIH Atrial Fibrillation Database (AFDB)
PhysioNet page: https://physionet.org/content/afdb/1.0.0/
**Records used:** `04015, 04043, 04048, 04126, 04746, 04936, 05091`

### 3) MI — PTB Diagnostic ECG Database (PTB-DB)
PhysioNet page: https://physionet.org/content/ptbdb/1.0.0/
**Records used:** 
`patient014/s0046lre, patient013/s0045lre, patient006/s0022lre, 
patient007/s0026lre, patient008/s0028lre, patient002/s0015lre, 
patient011/s0039lre, patient012/s0043lre`

> **Note:** Please respect each dataset's license/citation policy on PhysioNet.

## How to Reproduce 
1. Clone the repo:
   ```bash
   git clone <your-repo-url>.git
   cd <repo-name>
   ```
2. Create environment & install deps:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # on Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Prepare folders and place signals **(or download from PhysioNet)**:
   ```
   data/
     normal/   # NSRDB records listed above
     afib/     # AFDB records listed above
     MI/       # PTB-DB records listed above
   ```
4. Run the pipeline (baseline):
   ```bash
   python main.py
   ```
   - This will: build per-class CSVs → clean AFib windows → merge → train Decision Tree → print a classification report.

## Repository Structure 
```
ecg-ecg-classification/
├─ main.py
├─ requirements.txt
├─ README.md
├─ CODEBOOK.md                  # to be added
├─ exploration.ipynb            # to be added (plots + model comparisons)
├─ ecg_utils/
│  ├─ __init__.py
│  ├─ segmenter.py
│  ├─ feature_extractor.py
│  ├─ dataset_builder.py
│  └─ afib_filter.py
└─ data/                        # not tracked by git
   ├─ normal/
   ├─ afib/
   └─ MI/
```



*Maintainer:* Hasan Soliman
