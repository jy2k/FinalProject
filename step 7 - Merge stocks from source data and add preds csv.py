# This script merges all the original stock data into one big file that has all the stocks.
import pandas as pd
list_of_columns = ['Date', 'Adj Close', 'adj_1', 'adj_7', 'adj_30','adj_90', 'adj_1_change', 'adj_7_change', 'adj_30_change','adj_90_change', 'avg_adj_1_change']

stock='AFRM'
list_of_new_cols = ['Date', f'{stock}_Adj Close', f'{stock}_adj_1', f'{stock}_adj_7', f'{stock}_adj_30','adj_90', f'{stock}_adj_1_change', f'{stock}_adj_7_change', f'{stock}_adj_30_change',f'{stock}_adj_90_change', f'{stock}_avg_adj_1_change']

# Load the first CSV file into a DataFrame
df1 = pd.read_csv('stocks source data/AFRM.csv')

# Select specific columns from the first DataFrame
df1 = df1[list_of_columns]

# Rename the columns of the first DataFrame
df1.columns = list_of_new_cols

stock='LC'
list_of_new_cols = ['Date', f'{stock}_Adj Close', f'{stock}_adj_1', f'{stock}_adj_7', f'{stock}_adj_30','adj_90', f'{stock}_adj_1_change', f'{stock}_adj_7_change', f'{stock}_adj_30_change',f'{stock}_adj_90_change', f'{stock}_avg_adj_1_change']

# Load the second CSV file into a DataFrame
df2 = pd.read_csv('stocks source data/LC.csv')

# Select specific columns from the second DataFrame
df2 = df2[list_of_columns]

# Rename the columns of the second DataFrame
df2.columns = list_of_new_cols


stock='OPRT'
list_of_new_cols = ['Date', f'{stock}_Adj Close', f'{stock}_adj_1', f'{stock}_adj_7', f'{stock}_adj_30','adj_90', f'{stock}_adj_1_change', f'{stock}_adj_7_change', f'{stock}_adj_30_change',f'{stock}_adj_90_change', f'{stock}_avg_adj_1_change']

# Load the third CSV file into a DataFrame
df3 = pd.read_csv('stocks source data/OPRT.csv')

# Select specific columns from the third DataFrame
df3 = df3[list_of_columns]

# Rename the columns of the third DataFrame
df3.columns = list_of_new_cols

stock='SOFI'
list_of_new_cols = ['Date', f'{stock}_Adj Close', f'{stock}_adj_1', f'{stock}_adj_7', f'{stock}_adj_30','adj_90', f'{stock}_adj_1_change', f'{stock}_adj_7_change', f'{stock}_adj_30_change',f'{stock}_adj_90_change', f'{stock}_avg_adj_1_change']


# Load the fourth CSV file into a DataFrame
df4 = pd.read_csv('stocks source data/SOFI.csv')

# Select specific columns from the fourth DataFrame
df4 = df4[list_of_columns]

# Rename the columns of the fourth DataFrame
df4.columns = list_of_new_cols


stock='UPST'
list_of_new_cols = ['Date', f'{stock}_Adj Close', f'{stock}_adj_1', f'{stock}_adj_7', f'{stock}_adj_30','adj_90', f'{stock}_adj_1_change', f'{stock}_adj_7_change', f'{stock}_adj_30_change',f'{stock}_adj_90_change', f'{stock}_avg_adj_1_change']


# Load the fifth CSV file into a DataFrame
df5 = pd.read_csv('stocks source data/UPST.csv')

# Select specific columns from the fifth DataFrame
df5 = df5[list_of_columns]

# Rename the columns of the fifth DataFrame
df5.columns = list_of_new_cols

# Merge the first and second DataFrames based on the date column
result1 = pd.merge(df1, df2, on='Date')

# Merge the third and fourth DataFrames based on the date column
result2 = pd.merge(df3, df4, on='Date')

# Merge the result of the previous merge with the fifth DataFrame based on the date column
result3 = pd.merge(result1, result2, on='Date')
result4 = pd.merge(result3, df5, on='Date')

# Save the merged DataFrame to a new CSV file
result4.to_csv('merged_all_stocks_source_data.csv', index=False)


# Create a list of 5 items
stock_list = ['AFRM', 'LC', 'OPRT', 'SOFI', 'UPST']

df_merged = result4

# Loop over the list
for stock in stock_list:
    print(stock)

    df_current_stock = pd.read_csv(str(stock+"_preds.csv"))

    df_merged = pd.merge(df_current_stock, df_merged, on="Date", how="right")
    print("test")
df_merged = df_merged[['Date','UPST_adj_1_change_pred', 'SOFI_adj_1_change_pred', 'OPRT_adj_1_change_pred', 'LC_adj_1_change_pred', 'AFRM_adj_1_change_pred', 'AFRM_adj_1_change', 'LC_adj_1_change', 'OPRT_adj_1_change', 'SOFI_adj_1_change', 'UPST_adj_1_change', 'AFRM_avg_adj_1_change']]

df_merged = df_merged.rename(columns={'AFRM_avg_adj_1_change': 'benchmark_avg_adj_1_change'})

df_merged['Date'] = pd.to_datetime(df_merged['Date'])

# Select all rows where the date in the 'Date' column is after '2022-01-02'
df_merged = df_merged.loc[df_merged['Date'] > '2021-11-29']
df_merged = df_merged.sort_values(by='Date')
# Write the merged dataframe to a new CSV file
df_merged.to_csv("merged_file.csv", index=False)