import numpy as np
import pandas as pd

tn = pd.read_csv("../data/tn_synthetic_crop_data.csv")

augmented = []

for _, row in tn.iterrows():
    for _ in range(15):  # create 15 variants per row
        new_row = row.copy()
        new_row["Temperature"] += np.random.normal(0, 1.0)
        new_row["Rainfall"] += np.random.normal(0, 15)
        new_row["Humidity"] += np.random.normal(0, 3)
        new_row["N"] += np.random.normal(0, 5)
        new_row["P"] += np.random.normal(0, 3)
        new_row["K"] += np.random.normal(0, 3)
        augmented.append(new_row)

aug_df = pd.DataFrame(augmented)
aug_df.to_csv("../data/tn_augmented_crop_data.csv", index=False)

print("New size:", aug_df.shape)
