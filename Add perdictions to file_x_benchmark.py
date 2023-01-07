import pandas as pd

# Create a list of 5 items
stock_list = ['AFRM', 'LC', 'OPRT', 'SOFI', 'UPST']

df_merged = pd.read_csv("merged_all_stocks_source_data.csv")

# Loop over the list
for stock in stock_list:
    print(stock)

    df_current_stock = pd.read_csv(str(stock+"_preds.csv"))

    df_merged = pd.merge(df_current_stock, df_merged, on="Date", how="outer")

# Write the merged dataframe to a new CSV file
df_merged.to_csv("merged_file.csv", index=False)
