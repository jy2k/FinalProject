# This script changes naming of columns so that those can be handled by regression code
import pandas as pd

afrm_fin_full = pd.read_csv('Output data/finsight/AFRM/finsight_with_stock_with_benchmark.csv', index_col=0)
lc_fin_full = pd.read_csv('Output data/finsight/LC/finsight_with_stock_with_benchmark.csv', index_col=0)
oprt_fin_full = pd.read_csv('Output data/finsight/OPRT/finsight_with_stock_with_benchmark.csv', index_col=0)
sofi_fin_full = pd.read_csv('Output data/finsight/SOFI/finsight_with_stock_with_benchmark.csv', index_col=0)
upst_fin_full = pd.read_csv('Output data/finsight/UPST/finsight_with_stock_with_benchmark.csv', index_col=0)

df_list = [afrm_fin_full, oprt_fin_full, sofi_fin_full, upst_fin_full, lc_fin_full]

for df in df_list:
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.str.replace('+', '')
    df.columns = df.columns.str.replace('-', '_')
    df.columns = df.columns.str.replace('(', '')
    df.columns = df.columns.str.replace(')', '')

afrm_fin_full.to_csv(f'Output data/finsight/AFRM/finsight_with_stock_with_benchmark.csv')
oprt_fin_full.to_csv(f'Output data/finsight/OPRT/finsight_with_stock_with_benchmark.csv')
sofi_fin_full.to_csv(f'Output data/finsight/SOFI/finsight_with_stock_with_benchmark.csv')
upst_fin_full.to_csv(f'Output data/finsight/UPST/finsight_with_stock_with_benchmark.csv')
lc_fin_full.to_csv(f'Output data/finsight/LC/finsight_with_stock_with_benchmark.csv')




