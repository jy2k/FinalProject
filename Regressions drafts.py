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

### AFRM ########################################## AFRM ######################################## AFRM ################

afrm_cohort_stock1 = pd.read_csv(f'Output data/cohort stock/AFRM/file_0_benchmark.csv')
afrm_cohort_stock2 = pd.read_csv(f'Output data/cohort stock/AFRM/file_1_benchmark.csv')
afrm_cohort_stock3 = pd.read_csv(f'Output data/cohort stock/AFRM/file_2_benchmark.csv')

afrm_deals = [afrm_cohort_stock1, afrm_cohort_stock2] #afrm_cohort_stock3

for df in afrm_deals:
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.str.replace('+', '')
    df['Gross_Coupon_Minus_Annualized_Net_Loss_Rate'] = df['Gross_Coupon'].subtract(df['Annualized_Net_Loss_Rate'])
    df['d1_dist_from_bench'] = df['adj_1_change'] - df['avg_adj_1_change']
    df['d7_dist_from_bench'] = df['adj_7_change'] - df['avg_adj_7_change']
    df['d30_dist_from_bench'] = df['adj_30_change'] - df['avg_adj_30_change']
    df['d90_dist_from_bench'] = df['adj_90_change'] - df['avg_adj_90_change']
    # df['d1_Vol'] = df['adj_1_change'] ** 2
    # df['d7_Vol'] = df['adj_7_change'] ** 2
    # df['d30_Vol'] = df['adj_30_change'] ** 2
    # df['d90_Vol'] = df['adj_90_change'] ** 2
    # df['d1_BenchVol'] = df['avg_adj_1_change'] ** 2
    # df['d7_BenchVol'] = df['avg_adj_7_change'] ** 2
    # df['d30_BenchVol'] = df['avg_adj_30_change'] ** 2
    # df['d90_BenchVol'] = df['avg_adj_90_change'] ** 2
    # df['d1_ExcessVol'] = df['d1_Vol'] - df['d1_BenchVol']
    # df['d7_ExcessVol'] = df['d7_Vol'] - df['d7_BenchVol']
    # df['d30_ExcessVol'] = df['d30_Vol'] - df['d30_BenchVol']
    # df['d90_ExcessVol'] = df['d90_Vol'] - df['d90_BenchVol']

afrm_cohort_stock_combined = pd.concat(afrm_deals, ignore_index=True, sort=False)

afrm_costock_combine_bench_rsquared = []
for i in ['d1_dist_from_bench', 'd7_dist_from_bench', 'd30_dist_from_bench', 'd90_dist_from_bench']:
    results = smf.ols(f'{i} ~ Annualized_Net_Loss_Rate + Life_CDR', data=afrm_cohort_stock_combined).fit()
    print(results.summary())
    afrm_costock_combine_bench_rsquared.append(results.rsquared)
print(afrm_costock_combine_bench_rsquared)

afrm_costock_combine_change_rsquared = []
for i in ['adj_1_change', 'adj_7_change', 'adj_30_change', 'adj_90_change']:
    results = smf.ols(f'{i} ~ Annualized_Net_Loss_Rate + Life_CDR', data=afrm_cohort_stock_combined).fit()
    print(results.summary())
    afrm_costock_combine_change_rsquared.append(results.rsquared)
print(afrm_costock_combine_change_rsquared)
print(afrm_costock_combine_bench_rsquared)


x = ['1d', '7d', '30d', '90d']

plt.plot(x, afrm_costock_combine_change_rsquared, label ="stock change", color ="blue")
plt.plot(x, afrm_costock_combine_bench_rsquared, label ="Benchmark", color ="green")
plt.title('AFRM R^2 for % change and Benchmark in stock')
plt.ylabel('R^2')
plt.grid()
plt.legend()
plt.show()

# for i in afrm_deals:
#     plt.plot(i['Annualized_Net_Loss_Rate'])
#     plt.show()

###### Checking for Volatility #######
afrm_costock_vol_combine_change_rsquared = []
for i in ['d1_Vol', 'd7_Vol', 'd30_Vol', 'd90_Vol']:
    results = smf.ols(f'{i} ~ Annualized_Net_Loss_Rate + Life_CDR', data=afrm_cohort_stock_combined).fit()
    print(results.summary())
    afrm_costock_vol_combine_change_rsquared.append(results.rsquared)

afrm_costock_vol_combine_bench_rsquared = []
for i in ['d1_ExcessVol', 'd7_ExcessVol', 'd30_ExcessVol', 'd90_ExcessVol']:
    results = smf.ols(f'{i} ~ Annualized_Net_Loss_Rate + Life_CDR', data=afrm_cohort_stock_combined).fit()
    print(results.summary())
    afrm_costock_vol_combine_bench_rsquared.append(results.rsquared)


print(afrm_costock_vol_combine_change_rsquared)
print(afrm_costock_vol_combine_bench_rsquared)

plt.plot(x, afrm_costock_vol_combine_change_rsquared, label ="Volatility", color ="blue")
plt.plot(x, afrm_costock_vol_combine_bench_rsquared, label ="ExcessVolatility", color ="green")
plt.title('AFRM R^2 for Volatility and ExcessVolatility')
plt.ylabel('R^2')
plt.grid()
plt.legend()
plt.show()

plt.plot(afrm_cohort_stock_combined['Date'].values, afrm_cohort_stock_combined['d1_Vol'].values, label ="Volatility", color ="blue")
plt.plot(afrm_cohort_stock_combined['Date'].values, afrm_cohort_stock_combined['d1_BenchVol'].values, label ="BenchVol", color ="grey")
plt.title('AFRM Volatility and BenchVol')
plt.ylabel('Volatility')
plt.grid()
plt.legend()
plt.show()


# ### LC ########################################## LC ######################################## LC ##################
#
# lc_cohort_stock1 = pd.read_csv(f'Output data/cohort stock/LC/file_0_benchmark.csv')
# lc_cohort_stock2 = pd.read_csv(f'Output data/cohort stock/LC/file_1_benchmark.csv')
# lc_cohort_stock3 = pd.read_csv(f'Output data/cohort stock/LC/file_2_benchmark.csv')
#
# lc_deals = [lc_cohort_stock1,lc_cohort_stock3] # lc_cohort_stock2
#
# for df in lc_deals:
#     df.columns = df.columns.str.replace(' ', '_')
#     df.columns = df.columns.str.replace('+', '')
#     df['Gross_Coupon_Minus_Annualized_Net_Loss_Rate'] = df['Gross_Coupon'].subtract(df['Annualized_Net_Loss_Rate'])
#     df['d1_dist_from_bench'] = df['adj_1_change'] - df['avg_adj_1_change']
#     df['d7_dist_from_bench'] = df['adj_7_change'] - df['avg_adj_7_change']
#     df['d30_dist_from_bench'] = df['adj_30_change'] - df['avg_adj_30_change']
#     df['d90_dist_from_bench'] = df['adj_90_change'] - df['avg_adj_90_change']
#
# lc_cohort_stock_combined = pd.concat(lc_deals, ignore_index=True, sort=False)
#
# lc_costock_combine_bench_rsquared = []
# for i in ['d1_dist_from_bench', 'd7_dist_from_bench', 'd30_dist_from_bench', 'd90_dist_from_bench']:
#     results = smf.ols(f'{i} ~ Gross_Coupon_Minus_Annualized_Net_Loss_Rate + Life_CDR', data=lc_cohort_stock_combined).fit()
#     print(results.summary())
#     lc_costock_combine_bench_rsquared.append(results.rsquared)
# print(lc_costock_combine_bench_rsquared)
#
# lc_costock_combine_change_rsquared = []
# for i in ['adj_1_change', 'adj_7_change', 'adj_30_change', 'adj_90_change']:
#     results = smf.ols(f'{i} ~ Gross_Coupon_Minus_Annualized_Net_Loss_Rate + Life_CDR', data=lc_cohort_stock_combined).fit()
#     print(results.summary())
#     lc_costock_combine_change_rsquared.append(results.rsquared)
# print(lc_costock_combine_change_rsquared)
# print(lc_costock_combine_bench_rsquared)
#
#
# x = ['1d', '7d', '30d', '90d']
#
# plt.plot(x, lc_costock_combine_change_rsquared, label ="stock change", color ="blue")
# plt.plot(x, lc_costock_combine_bench_rsquared, label ="Benchmark", color ="green")
# plt.title('LC R^2 for % change and Benchmark in stock')
# plt.ylabel('R^2')
# plt.grid()
# plt.legend()
# plt.show()
#
# for i in lc_deals:
#     plt.plot(i['Gross_Coupon_Minus_Annualized_Net_Loss_Rate'])
#     plt.show()
#
#
# ### OPRT ########################################## OPRT ######################################## OPRT ##################
#
# oprt_cohort_stock1 = pd.read_csv(f'Output data/cohort stock/OPRT/file_0_benchmark.csv')
# oprt_cohort_stock2 = pd.read_csv(f'Output data/cohort stock/OPRT/file_1_benchmark.csv')
# oprt_cohort_stock3 = pd.read_csv(f'Output data/cohort stock/OPRT/file_2_benchmark.csv')
#
# oprt_deals = [oprt_cohort_stock1, oprt_cohort_stock3] #oprt_cohort_stock2
#
# for df in oprt_deals:
#     df.columns = df.columns.str.replace(' ', '_')
#     df.columns = df.columns.str.replace('+', '')
#     df['Gross_Coupon_Minus_Annualized_Net_Loss_Rate'] = df['Gross_Coupon'].subtract(df['Annualized_Net_Loss_Rate'])
#     df['d1_dist_from_bench'] = df['adj_1_change'] - df['avg_adj_1_change']
#     df['d7_dist_from_bench'] = df['adj_7_change'] - df['avg_adj_7_change']
#     df['d30_dist_from_bench'] = df['adj_30_change'] - df['avg_adj_30_change']
#     df['d90_dist_from_bench'] = df['adj_90_change'] - df['avg_adj_90_change']
#
# oprt_cohort_stock_combined = pd.concat(oprt_deals, ignore_index=True, sort=False)
#
# oprt_costock_combine_bench_rsquared = []
# for i in ['d1_dist_from_bench', 'd7_dist_from_bench', 'd30_dist_from_bench', 'd90_dist_from_bench']:
#     results = smf.ols(f'{i} ~ Gross_Coupon_Minus_Annualized_Net_Loss_Rate + Life_CDR', data=oprt_cohort_stock_combined).fit()
#     print(results.summary())
#     oprt_costock_combine_bench_rsquared.append(results.rsquared)
# print(oprt_costock_combine_bench_rsquared)
#
# oprt_costock_combine_change_rsquared = []
# for i in ['adj_1_change', 'adj_7_change', 'adj_30_change', 'adj_90_change']:
#     results = smf.ols(f'{i} ~ Gross_Coupon_Minus_Annualized_Net_Loss_Rate + Life_CDR', data=oprt_cohort_stock_combined).fit()
#     print(results.summary())
#     oprt_costock_combine_change_rsquared.append(results.rsquared)
# print(oprt_costock_combine_change_rsquared)
# print(oprt_costock_combine_bench_rsquared)
#
#
# x = ['1d', '7d', '30d', '90d']
#
# plt.plot(x, oprt_costock_combine_change_rsquared, label ="stock change", color ="blue")
# plt.plot(x, oprt_costock_combine_bench_rsquared, label ="Benchmark", color ="green")
# plt.title('oprt R^2 for % change and Benchmark in stock')
# plt.ylabel('R^2')
# plt.grid()
# plt.legend()
# plt.show()
#
# for i in oprt_deals:
#     plt.plot(i['Gross_Coupon_Minus_Annualized_Net_Loss_Rate'])
#     plt.show()
#
# ### SOFI ########################################## SOFI ######################################## SOFI ##################
#
# sofi_cohort_stock1 = pd.read_csv(f'Output data/cohort stock/SOFI/file_0_benchmark.csv')
# sofi_cohort_stock2 = pd.read_csv(f'Output data/cohort stock/SOFI/file_1_benchmark.csv')
# sofi_cohort_stock3 = pd.read_csv(f'Output data/cohort stock/SOFI/file_2_benchmark.csv')
#
# upst_deals = [sofi_cohort_stock1, sofi_cohort_stock3] # lc_cohort_stock2
#
# for df in upst_deals:
#     df.columns = df.columns.str.replace(' ', '_')
#     df.columns = df.columns.str.replace('+', '')
#     df['Gross_Coupon_Minus_Annualized_Net_Loss_Rate'] = df['Gross_Coupon'].subtract(df['Annualized_Net_Loss_Rate'])
#     df['d1_dist_from_bench'] = df['adj_1_change'] - df['avg_adj_1_change']
#     df['d7_dist_from_bench'] = df['adj_7_change'] - df['avg_adj_7_change']
#     df['d30_dist_from_bench'] = df['adj_30_change'] - df['avg_adj_30_change']
#     df['d90_dist_from_bench'] = df['adj_90_change'] - df['avg_adj_90_change']
#
# sofi_cohort_stock_combined = pd.concat(upst_deals, ignore_index=True, sort=False)
#
# sofi_costock_combine_bench_rsquared = []
# for i in ['d1_dist_from_bench', 'd7_dist_from_bench', 'd30_dist_from_bench', 'd90_dist_from_bench']:
#     results = smf.ols(f'{i} ~ Gross_Coupon_Minus_Annualized_Net_Loss_Rate + Life_CDR', data=sofi_cohort_stock_combined).fit()
#     print(results.summary())
#     sofi_costock_combine_bench_rsquared.append(results.rsquared)
# print(sofi_costock_combine_bench_rsquared)
#
# sofi_costock_combine_change_rsquared = []
# for i in ['adj_1_change', 'adj_7_change', 'adj_30_change', 'adj_90_change']:
#     results = smf.ols(f'{i} ~ Gross_Coupon_Minus_Annualized_Net_Loss_Rate + Life_CDR', data=sofi_cohort_stock_combined).fit()
#     print(results.summary())
#     sofi_costock_combine_change_rsquared.append(results.rsquared)
# print(sofi_costock_combine_change_rsquared)
# print(sofi_costock_combine_bench_rsquared)
#
#
# x = ['1d', '7d', '30d', '90d']
#
# plt.plot(x, sofi_costock_combine_change_rsquared, label ="stock change", color ="blue")
# plt.plot(x, sofi_costock_combine_bench_rsquared, label ="Benchmark", color ="green")
# plt.title('sofi R^2 for % change and Benchmark in stock')
# plt.ylabel('R^2')
# plt.grid()
# plt.legend()
# plt.show()
#
# for i in upst_deals:
#     plt.plot(i['Gross_Coupon_Minus_Annualized_Net_Loss_Rate'])
#     plt.show()
#
# ### UPST ########################################## UPST ######################################## UPST ##################
#
# upst_cohort_stock1 = pd.read_csv(f'Output data/cohort stock/UPST/file_0_benchmark.csv')
# upst_cohort_stock2 = pd.read_csv(f'Output data/cohort stock/UPST/file_1_benchmark.csv')
# upst_cohort_stock3 = pd.read_csv(f'Output data/cohort stock/UPST/file_2_benchmark.csv')
# upst_cohort_stock4 = pd.read_csv(f'Output data/cohort stock/UPST/file_2_benchmark.csv')
#
#
# upst_deals = [upst_cohort_stock1, upst_cohort_stock2, upst_cohort_stock3, upst_cohort_stock4]
#
# for df in upst_deals:
#     df.columns = df.columns.str.replace(' ', '_')
#     df.columns = df.columns.str.replace('+', '')
#     df['Gross_Coupon_Minus_Annualized_Net_Loss_Rate'] = df['Gross_Coupon'].subtract(df['Annualized_Net_Loss_Rate'])
#     df['d1_dist_from_bench'] = df['adj_1_change'] - df['avg_adj_1_change']
#     df['d7_dist_from_bench'] = df['adj_7_change'] - df['avg_adj_7_change']
#     df['d30_dist_from_bench'] = df['adj_30_change'] - df['avg_adj_30_change']
#     df['d90_dist_from_bench'] = df['adj_90_change'] - df['avg_adj_90_change']
#
# upst_cohort_stock_combined = pd.concat(upst_deals, ignore_index=True, sort=False)
#
# upst_costock_combine_bench_rsquared = []
# for i in ['d1_dist_from_bench', 'd7_dist_from_bench', 'd30_dist_from_bench', 'd90_dist_from_bench']:
#     results = smf.ols(f'{i} ~ Gross_Coupon_Minus_Annualized_Net_Loss_Rate + Life_CDR', data=upst_cohort_stock_combined).fit()
#     print(results.summary())
#     upst_costock_combine_bench_rsquared.append(results.rsquared)
# print(upst_costock_combine_bench_rsquared)
#
# upst_costock_combine_change_rsquared = []
# for i in ['adj_1_change', 'adj_7_change', 'adj_30_change', 'adj_90_change']:
#     results = smf.ols(f'{i} ~ Gross_Coupon_Minus_Annualized_Net_Loss_Rate + Life_CDR', data=upst_cohort_stock_combined).fit()
#     print(results.summary())
#     upst_costock_combine_change_rsquared.append(results.rsquared)
# print(upst_costock_combine_change_rsquared)
# print(upst_costock_combine_bench_rsquared)
#
#
# x = ['1d', '7d', '30d', '90d']
#
# plt.plot(x, upst_costock_combine_change_rsquared, label ="stock change", color ="blue")
# plt.plot(x, upst_costock_combine_bench_rsquared, label ="Benchmark", color ="green")
# plt.title('upst R^2 for % change and Benchmark in stock')
# plt.ylabel('R^2')
# plt.grid()
# plt.legend()
# plt.show()
#
# for i in upst_deals:
#     plt.plot(i['Gross_Coupon_Minus_Annualized_Net_Loss_Rate'])
#     plt.show()
#
# #### All cohort deals ####
#
# combined_cohort_deals = [afrm_cohort_stock_combined, upst_cohort_stock_combined, afrm_cohort_stock_combined,
#                    oprt_cohort_stock_combined, lc_cohort_stock_combined]
#
# all_issuers_cohort_stocks = pd.concat(combined_cohort_deals, ignore_index=True, sort=False)
#
# all_costock_combine_bench_rsquared = []
# for i in ['d1_dist_from_bench', 'd7_dist_from_bench', 'd30_dist_from_bench', 'd90_dist_from_bench']:
#     results = smf.ols(f'{i} ~ Gross_Coupon_Minus_Annualized_Net_Loss_Rate + Life_CDR', data=all_issuers_cohort_stocks).fit()
#     print(results.summary())
#     all_costock_combine_bench_rsquared.append(results.rsquared)
# print(all_costock_combine_bench_rsquared)
#
# all_costock_combine_change_rsquared = []
# for i in ['adj_1_change', 'adj_7_change', 'adj_30_change', 'adj_90_change']:
#     results = smf.ols(f'{i} ~ Gross_Coupon_Minus_Annualized_Net_Loss_Rate + Life_CDR', data=all_issuers_cohort_stocks).fit()
#     print(results.summary())
#     all_costock_combine_change_rsquared.append(results.rsquared)
# print(all_costock_combine_change_rsquared)
# print(all_costock_combine_bench_rsquared)
#
#
# x = ['1d', '7d', '30d', '90d']
#
# plt.plot(x, all_costock_combine_change_rsquared, label ="stock change", color ="blue")
# plt.plot(x, all_costock_combine_bench_rsquared, label ="Benchmark", color ="green")
# plt.title('all R^2 for % change and Benchmark in stock')
# plt.ylabel('R^2')
# plt.grid()
# plt.legend()
# plt.show()

# plt.scatter(df_combined_files['adj_7_change'], df_combined_files['Annualized_Net_Loss_Rate'], alpha=0.5)
# plt.title('Scatter plot of Annualized_Net_Loss_Rate with adj_7_change')
# plt.xlabel('adj_7_change')
# plt.ylabel('Annualized_Net_Loss_Rate')
# plt.show()



