import pandas as pd
import glob

train_files = glob.glob(r"D:\ETL astro\data\Ecommerce Order Dataset\train\*.csv")
test_files = glob.glob(r"D:\ETL astro\data\Ecommerce Order Dataset\test\*.csv")

train_df = pd.concat([pd.read_csv(f) for f in train_files], ignore_index=True)
test_df = pd.concat([pd.read_csv(f) for f in test_files], ignore_index=True)


print(train_df.shape, test_df.shape)