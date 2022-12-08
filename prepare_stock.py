import pandas as pd

dict_of_finsight_files = {'AFRM': 'stocks/AFRM.csv',
                          'LC': 'stocks/LC.csv',
                          'OPRT': 'stocks/OPRT.csv',
                          'SOFI': 'stocks/SOFI.csv',
                          'UPST': 'stocks/UPST.csv'}
for stock, file in dict_of_finsight_files.items():
    df_stock = pd.read_csv(file)

    df_stock.sort_values('Date', inplace=True)
    df_stock['adj_1'] = df_stock['Adj Close'].shift(-1)
    df_stock['adj_7'] = df_stock['Adj Close'].shift(-5)
    df_stock['adj_30'] = df_stock['Adj Close'].shift(-22)
    df_stock['adj_90'] = df_stock['Adj Close'].shift(-66)

    df_stock.to_csv(file)