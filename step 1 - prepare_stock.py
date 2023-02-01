# This script takes the original stocks data
# it adds all the column such ad adj_x (essentially the rest aren't used)
import pandas as pd

dict_of_stock_files = {'AFRM': 'stocks source data/AFRM.csv',
                          'LC': 'stocks source data/LC.csv',
                          'OPRT': 'stocks source data/OPRT.csv',
                          'SOFI': 'stocks source data/SOFI.csv',
                          'UPST': 'stocks source data/UPST.csv'}

df_benchmark = pd.DataFrame()
date_range = pd.date_range(start ='12-1-2014',end ='11-23-2022', freq ='1D')
print(date_range[0])
print(date_range[-1])
df_benchmark['Date'] = date_range.astype('datetime64[ns]')

for stock, file in dict_of_stock_files.items():
    df_stock = pd.read_csv(file)

    df_stock.sort_values('Date', inplace=True)
    df_stock['adj_1'] = df_stock['Adj Close'].shift(-1)
    df_stock['adj_7'] = df_stock['Adj Close'].shift(-5)
    df_stock['adj_30'] = df_stock['Adj Close'].shift(-22)
    df_stock['adj_90'] = df_stock['Adj Close'].shift(-66)
    df_stock = df_stock[df_stock.columns.drop(list(df_stock.filter(regex='Unnamed*')))]

    df_stock['adj_1_change'] = (df_stock['adj_1']/df_stock['Adj Close'])-1
    df_stock['adj_7_change'] = (df_stock['adj_7']/df_stock['Adj Close'])-1
    df_stock['adj_30_change'] = (df_stock['adj_30']/df_stock['Adj Close'])-1
    df_stock['adj_90_change'] = (df_stock['adj_90']/df_stock['Adj Close'])-1

    df_stock['d1_Vol'] = df_stock['adj_1_change'] ** 2
    df_stock['d7_Vol'] = df_stock['adj_7_change'] ** 2
    df_stock['d30_Vol'] = df_stock['adj_30_change'] ** 2
    df_stock['d90_Vol'] = df_stock['adj_90_change'] ** 2
    df_stock['d1_BenchVol'] = df_stock['avg_adj_1_change'] ** 2
    df_stock['d7_BenchVol'] = df_stock['avg_adj_7_change'] ** 2
    df_stock['d30_BenchVol'] = df_stock['avg_adj_30_change'] ** 2
    df_stock['d90_BenchVol'] = df_stock['avg_adj_90_change'] ** 2
    df_stock['d1_ExcessVol'] = df_stock['d1_Vol'] - df_stock['d1_BenchVol']
    df_stock['d7_ExcessVol'] = df_stock['d7_Vol'] - df_stock['d7_BenchVol']
    df_stock['d30_ExcessVol'] = df_stock['d30_Vol'] - df_stock['d30_BenchVol']
    df_stock['d90_ExcessVol'] = df_stock['d90_Vol'] - df_stock['d90_BenchVol']
    df_stock.to_csv(file)
    df_stock.set_index('Date')

    df_temp = pd.DataFrame()
    df_temp['Date_temp'] = df_stock['Date'].astype('datetime64[ns]')
    df_temp.set_index('Date_temp')
    df_temp[f'{stock}_adj_1_change'] = df_stock['adj_1'].pct_change()
    df_temp[f'{stock}_adj_7_change'] = df_stock['adj_7'].pct_change()
    df_temp[f'{stock}_adj_30_change'] = df_stock['adj_30'].pct_change()
    df_temp[f'{stock}_adj_90_change'] = df_stock['adj_90'].pct_change()

    df_benchmark = df_benchmark.merge(df_temp, how='left', left_on='Date', right_on='Date_temp')

# for i in ['_adj_1_change', '_adj_7_change', '_adj_30_change', '_adj_90_change']:
#     df_benchmark['avg'+i] =df_benchmark[['AFRM'+i, 'LC'+i, 'UPST'+i, 'SOFI'+i,'OPRT'+i]].mean(axis=1)

df_benchmark.to_csv('Output data/benchmark.csv')
df_benchmark.drop(df_benchmark.columns.difference(['Date','avg_adj_1_change', 'avg_adj_7_change', 'avg_adj_30_change', 'avg_adj_90_change']), 1, inplace=True)
df_benchmark.to_csv('Output data/benchmark-clean.csv')

#add the benchmark to every stock that way it gets merged into the
#Left join on the stock per file.
for stock, file in dict_of_stock_files.items():
    df_benchmark = pd.read_csv('Output data/benchmark-clean.csv')
    df_stock = pd.read_csv(f'stocks source data/{stock}.csv')
    final_stock = df_stock.merge(df_benchmark, how='left', left_on='Date', right_on='Date')
    final_stock.to_csv(f'stocks source data/{stock}.csv')

print('end')