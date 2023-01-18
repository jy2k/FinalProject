# Merges the finsight data (with deltas) to stock (after cohort merge)
import pandas as pd


dict_cohort_files = {'AFRM': 'Output data/post feature eng/finsight_AFRM_with_deltas.csv',
                         'LC': 'Output data/post feature eng/finsight_LC_with_deltas.csv',
                        'OPRT': 'Output data/post feature eng/finsight_OPRT_with_deltas.csv',
                        'SOFI': 'Output data/post feature eng/finsight_SOFI_with_deltas.csv',
                        'UPST': 'Output data/post feature eng/finsight_UPST_with_deltas.csv'}

def manipulate(filename, stock):
    df_finsight = pd.read_csv(filename)
    df_finsight['Date'] =  pd.to_datetime(df_finsight['Date'], format='%Y-%m-%d')

    df_stock = pd.read_csv(f'stocks source data/{stock}.csv')
    df_stock['Date'] =  pd.to_datetime(df_stock['Date'], format='%Y-%m-%d')

    date_list = df_finsight['Date'].values

    df_stock.set_index('Date', inplace = True)
    #https://stackoverflow.com/a/22898920/1384948
    df_stock_filtered = df_stock[df_stock.index.isin(date_list)]

    df_finsight.set_index('Date', inplace = True)

    final = df_finsight.merge(df_stock_filtered, left_index=True, right_on='Date')

    return final

for stock, file in dict_cohort_files.items():
    final = manipulate(file, stock)
    final.to_csv(f'Output data/finsight/{stock}/finsight_with_stock_with_benchmark.csv')

print('end')