import pandas as pd
import statsmodels.formula.api as sm
import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels.formula.api as smf
from statsmodels.compat import lzip
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols

benchmarkdf = pd.DataFrame()

stocks_list = ['/Users/eyalben-eliyahu/PycharmProjects/FinalProject/stocks/AFRM.csv', '/Users/eyalben-eliyahu/PycharmProjects/FinalProject/stocks/LC.csv', '/Users/eyalben-eliyahu/PycharmProjects/FinalProject/stocks/OPRT.csv',
               '/Users/eyalben-eliyahu/PycharmProjects/FinalProject/stocks/SOFI.csv','/Users/eyalben-eliyahu/PycharmProjects/FinalProject/stocks/UPST.csv']

# for i in stocks_list:
#     df = pd.read_csv(i)
#     df['Adj Close 1d'] = df['Adj Close'].shift(-1)
#     df['Adj Close 1w'] = df['Adj Close'].shift(-5)
#     df['Adj Close 1m'] = df['Adj Close'].shift(-22)
#     df['Adj Close 3m'] = df['Adj Close'].shift(-66)
#     df.to_csv((f'{i}').replace('.csv', '')+'.csv')

for i in stocks_list:
    df = pd.read_csv(i)
    benchmarkdf[f'{i[-8:-4]}Adj Close 1d'] = df['Adj Close'].shift(-1)
    benchmarkdf[f'{i[-8:-4]}Adj Close 1w'] = df['Adj Close'].shift(-5)
    benchmarkdf[f'{i[-8:-4]}Adj Close 1m'] = df['Adj Close'].shift(-22)
    benchmarkdf[f'{i[-8:-4]}Adj Close 3m'] = df['Adj Close'].shift(-66)
    benchmarkdf.to_csv('benchmark.csv')

print(benchmarkdf)

for i in benchmarkdf.columns:
    benchmarkdf[f'{i}%change'] = benchmarkdf[i].pct_change()


benchmarkdf_pct = benchmarkdf.sub
benchmarkdf.to_csv('benchmarks_new_with_pct.csv')



print(benchmarkdf)




# benchmarkdf['1d_benchmark'] = benchmarkdf.iloc[:, [0,1,2,3,4]].mean(axis=1)