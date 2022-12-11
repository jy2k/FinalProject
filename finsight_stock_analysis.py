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
import seaborn as sn

afrm_fin_full = pd.read_csv(f'Output data/finsight/finsight_final_data_sets/afrm_fin_full.csv')
oprt_fin_full = pd.read_csv(f'Output data/finsight/finsight_final_data_sets/oprt_fin_full.csv')
sofi_fin_full = pd.read_csv(f'Output data/finsight/finsight_final_data_sets/sofi_fin_full.csv')
upst_fin_full = pd.read_csv(f'Output data/finsight/finsight_final_data_sets/upst_fin_full.csv')
# lc_fin_full = pd.read_csv(f'Output data/finsight/finsight_final_data_sets/lc_fin_full.csv')

finsight_interesting_columns = ['Sum_SZEM', 'CPN_A', 'PRICE_A', 'SPRD_A', 'SZEM_A', 'WAL_A', 'YLD_A',
                                'CPN_B', 'PRICE_B', 'SPRD_B', 'SZEM_B', 'WAL_B', 'YLD_B',
                                'CPN_C', 'PRICE_C', 'SPRD_C', 'SZEM_C', 'WAL_C', 'YLD_C']

### If there is D and E you are missing it

finsight_deltas = ['CPN_A_change', 'CPN_B_change', 'CPN_C_change', 'CPN_D_change', 'PRICE_A_change',
                   'PRICE_B_change', 'PRICE_C_change', 'PRICE_D_change', 'SPRD_A_change', 'SPRD_B_change',
                   'SPRD_C_change', 'SPRD_D_change', 'SZEM_A_change', 'SZEM_B_change', 'SZEM_C_change',
                   'SZEM_D_change', 'WAL_A_change', 'WAL_B_change', 'WAL_C_change',
                   'WAL_D_change', 'YLD_A_change', 'YLD_B_change', 'YLD_C_change', 'YLD_D_change']

finsight_stock_data = ['Adj_Close', 'adj_1', 'adj_7', 'adj_30', 'adj_90', 'adj_1_pct_chage', 'adj_7_pct_chage',
                       'adj_30_pct_chage', 'adj_90_pct_chage']

combined_list = finsight_interesting_columns + finsight_deltas + finsight_stock_data
explanatory_variables = finsight_interesting_columns + finsight_deltas


for i in finsight_interesting_columns:
    print(upst_fin_full['Sum_SZEM'].corr(upst_fin_full[i]), i)

sn.heatmap(upst_fin_full[combined_list].corr())
plt.show()

results = smf.ols('adj_1_pct_chage ~ CPN_A + PRICE_A + SPRD_A + WAL_A + YLD_A ', data=upst_fin_full).fit()
print(results.summary())

print(results.params)
print(results.rsquared_adj)

# rsquared_adj_list = []
# for i in ['adj_1_pct_chage', 'adj_7_pct_chage', 'adj_30_pct_chage', 'adj_90_pct_chage']:
#     results = smf.ols(f'{i} ~ CPN_A + PRICE_A + SPRD_A + WAL_A + YLD_A ', Output data=upst_fin_full).fit()
#     print(results.summary())
#     rsquared_adj_list.append(results.rsquared_adj)
# print(rsquared_adj_list)



rsquared_adj_list = []
for i in ['adj_1_pct_chage', 'adj_7_pct_chage', 'adj_30_pct_chage', 'adj_90_pct_chage']:
    results = smf.ols(f'{i} ~ Sum_SZEM + CPN_A + PRICE_A + SPRD_A + SZEM_A + WAL_A + YLD_A', data=upst_fin_full).fit()
    print(results.summary())
    rsquared_adj_list.append(results.rsquared_adj)
print(rsquared_adj_list)