import pandas as pd

# Read in the first CSV file
df1 = pd.read_csv("AFRM_preds.csv")

# Read in the second CSV file
df2 = pd.read_csv("merged_all_stocks_source_data.csv")

# Merge the two dataframes based on the Date column
df_merged = pd.merge(df1, df2, on="Date", how="outer")

# Write the merged dataframe to a new CSV file
df_merged.to_csv("merged_file.csv", index=False)
