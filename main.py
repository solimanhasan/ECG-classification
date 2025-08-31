# main.py 

from ecg_utils.dataset_builder import data_set
from ecg_utils.afib_filter import AfibCleaner
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


normal_signals = ["16265","16272","16273","16420","16483","16539","16773","16786","16795","17052"]
afib_signals = ["04015","04043","04048","04126","04746","04936","05091"]
mi_signals = [
    "patient014/s0046lre","patient013/s0045lre","patient006/s0022lre",
    "patient007/s0026lre","patient008/s0028lre",
    "patient002/s0015lre","patient011/s0039lre","patient012/s0043lre"
]


data_set(path="data/normal/", signal_names=normal_signals, channel_index=0, label=0, output_csv="normal.csv", fs=360, duration_minutes=2)
data_set(path="data/MI/", signal_names=mi_signals, channel_index=1, label=2, output_csv="mi.csv", fs=360, duration_minutes=2)
data_set(path="data/afib/", signal_names=afib_signals, channel_index=0, label=1, output_csv="afib.csv", fs=360, duration_minutes=6)


cleaner = AfibCleaner(reference_csv="normal.csv", features=["RR_std", "RMSSD", "HR_std"])
df_afib_clean = cleaner.clean("afib.csv", output_csv="afib_clean.csv")


df_normal = pd.read_csv("normal.csv")
df_afib = pd.read_csv("afib_clean.csv")
df_mi = pd.read_csv("mi.csv")

df_all = pd.concat([df_normal, df_afib, df_mi], ignore_index=True)
df_all.to_csv("final_dataset.csv", index=False)
print(f"Final dataset saved (n_samples={len(df_all)})")


X = df_all.drop(columns=["label"])
y = df_all["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = DecisionTreeClassifier()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print("\n=== Classification Report ===")
print(classification_report(y_test, y_pred))
