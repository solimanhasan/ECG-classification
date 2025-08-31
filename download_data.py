"""
download_data.py
----------------
Helper script to download ECG signals from PhysioNet.

Note:
- Records are stored under the following folders:
  data/normal/  → MIT-BIH Normal Sinus Rhythm Database (NSRDB)
  data/afib/    → MIT-BIH Atrial Fibrillation Database (AFDB)
  data/MI/      → PTB Diagnostic ECG Database (PTBDB)

- Make sure these folders exist (they will be created if missing).
- Each record usually consists of three files: .dat .hea .atr
- After downloading, you can directly run: python main.py
"""

import wfdb
import os

# === Record lists ===
normal_signals = [
    "16265","16272","16273","16420","16483",
    "16539","16773","16786","16795","17052"
]
afib_signals = [
    "04015","04043","04048","04126","04746","04936","05091"
]
mi_signals = [
    "patient014/s0046lre","patient013/s0045lre","patient006/s0022lre",
    "patient007/s0026lre","patient008/s0028lre",
    "patient002/s0015lre","patient011/s0039lre","patient012/s0043lre"
]

# === Database names on PhysioNet ===
DB_NORMAL = "mitdb"   # MIT-BIH Normal Sinus Rhythm Database
DB_AFIB   = "afdb"    # MIT-BIH Atrial Fibrillation Database
DB_MI     = "ptbdb"   # PTB Diagnostic ECG Database

def download_records(record_list, db_name, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    for rec in record_list:
        print(f"Downloading {rec} from {db_name} → {out_dir}")
        try:
            wfdb.dl_database(db_name, dl_dir=out_dir, records=[rec])
        except Exception as e:
            print(f"Error downloading {rec}: {e}")

if __name__ == "__main__":
    download_records(normal_signals, DB_NORMAL, "data/normal")
    download_records(afib_signals, DB_AFIB, "data/afib")
    download_records(mi_signals, DB_MI, "data/MI")

    print("\n✅ Download finished. Check 'data/' folders for signals.")
    print("Now you can run: python main.py")
