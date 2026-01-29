import pandas as pd

df = pd.read_csv('../data/tn_crop_recommendation_complete.csv')

print("Dataset Summary:")
print(f"Total samples: {len(df)}")
print(f"\nMissing values:\n{df.isnull().sum()}")
print(f"\nData types:\n{df.dtypes}")
print(f"\nNumerical summary:\n{df.describe()}")
