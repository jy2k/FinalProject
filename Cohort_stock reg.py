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

features_in_data = ['1mo_CPR', 'Gross_Coupon', 'Accum_Net_Loss%',
       'Annualized_Net_Loss_Rate', 'Delinq_30', 'Number_of_Assets',
       'Life_CDR', 'Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume',
       'Monthly_Change']

afrm_cohort_stock1 = pd.read_csv(f'Output data/cohort stock/AFRM/file_0_benchmark.csv')
afrm_cohort_stock2 = pd.read_csv(f'Output data/cohort stock/AFRM/file_1_benchmark.csv')
afrm_cohort_stock3 = pd.read_csv(f'Output data/cohort stock/AFRM/file_2_benchmark.csv')

afrm_deals = [afrm_cohort_stock1, afrm_cohort_stock2, afrm_cohort_stock3]

for df in afrm_deals:
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.str.replace('+', '')
    df['Gross_Coupon_Minus_Annualized_Net_Loss_Rate'] = df['Gross_Coupon'].subtract(df['Annualized_Net_Loss_Rate'])
    df['d1_dist_from_bench'] = df['adj_1_change'] - df['avg_adj_1_change']
    df['d7_dist_from_bench'] = df['adj_7_change'] - df['avg_adj_7_change']
    df['d30_dist_from_bench'] = df['adj_30_change'] - df['avg_adj_30_change']
    df['d90_dist_from_bench'] = df['adj_90_change'] - df['avg_adj_90_change']

afrm_cohort_stock1_rsquared = []
for i in ['d1_dist_from_bench', 'd7_dist_from_bench', 'd30_dist_from_bench', 'd90_dist_from_bench']:
    results = smf.ols(f'{i} ~ Gross_Coupon_Minus_Annualized_Net_Loss_Rate + Life_CDR', data=afrm_cohort_stock1).fit()
    # print(results.summary())
    afrm_cohort_stock1_rsquared.append(results.rsquared)
print(afrm_cohort_stock1_rsquared)

afrm_cohort_stock1_rsquared2 = []
for i in ['adj_1_change', 'adj_7_change', 'adj_30_change', 'adj_90_change']:
    results = smf.ols(f'{i} ~ Gross_Coupon_Minus_Annualized_Net_Loss_Rate + Life_CDR', data=afrm_cohort_stock1).fit()
    print(results.summary())
    afrm_cohort_stock1_rsquared2.append(results.rsquared)
print(afrm_cohort_stock1_rsquared2)
print(afrm_cohort_stock1_rsquared)


x = ['1d', '7d', '30d', '90d']

plt.plot(x, afrm_cohort_stock1_rsquared2, label = "stock change", color = "blue")
plt.plot(x, afrm_cohort_stock1_rsquared, label = "Benchmark", color = "green")
plt.title('R^2 for % change and Benchmark in stock')
plt.ylabel('R^2')
plt.grid()
plt.legend()
plt.show()



