import glob

import pandas as pd


ninds_files = sorted(glob.glob("data/*.csv"))
ninds_dfs = []
for file in ninds_files:
    df = pd.read_csv(file, encoding = "cp1252")
    ninds_dfs.append(df)
ninds_df = pd.concat(ninds_dfs, axis = 0)
ninds_df.to_csv('ninds_data.csv')
