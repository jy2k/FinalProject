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









##### Notice the LC is empty!! #####

# plt.rc("figure", figsize=(16, 8))
# plt.rc("font", size=14)
#
# plt.plot('Sum_SZE(M)', Output data = afrm_fin_full)



