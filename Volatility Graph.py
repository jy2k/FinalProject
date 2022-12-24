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
import matplotlib.dates as mdates

### Gather all stock data ###

afrm = pd.read_csv('stocks source data/AFRM.csv')
lc = pd.read_csv('stocks source data/LC.csv')
oprt = pd.read_csv('stocks source data/OPRT.csv')
sofi = pd.read_csv('stocks source data/SOFI.csv')
upst = pd.read_csv('stocks source data/UPST.csv')
all_stock_data=[afrm, lc, oprt, sofi, upst]


# for i in all_stock_data:
#     i['d1_Vol'] = i['adj_1_change'] ** 2
#     i['d7_Vol'] = i['adj_7_change'] ** 2
#     i['d30_Vol'] = i['adj_30_change'] ** 2
#     i['d90_Vol'] = i['adj_90_change'] ** 2
#     i['d1_BenchVol'] = i['avg_adj_1_change'] ** 2
#     i['d7_BenchVol'] = i['avg_adj_7_change'] ** 2
#     i['d30_BenchVol'] = i['avg_adj_30_change'] ** 2
#     i['d90_BenchVol'] = i['avg_adj_90_change'] ** 2
#     i['d1_ExcessVol'] = i['d1_Vol'] - i['d1_BenchVol']
#     i['d7_ExcessVol'] = i['d7_Vol'] - i['d7_BenchVol']
#     i['d30_ExcessVol'] = i['d30_Vol'] - i['d30_BenchVol']
#     i['d90_ExcessVol'] = i['d90_Vol'] - i['d90_BenchVol']

afrm_finsight_dates = pd.read_csv('Output data/finsight/AFRM/finsight_with_stock_with_benchmark.csv')['Date'].values
lc_finsight_dates = pd.read_csv('Output data/finsight/LC/finsight_with_stock_with_benchmark.csv')['Date'].values
oprt_finsight_dates = pd.read_csv('Output data/finsight/OPRT/finsight_with_stock_with_benchmark.csv')['Date'].values
sofi_finsight_dates = pd.read_csv('Output data/finsight/SOFI/finsight_with_stock_with_benchmark.csv')['Date'].values
upst_finsight_dates = pd.read_csv('Output data/finsight/UPST/finsight_with_stock_with_benchmark.csv')['Date'].values
finsight_dates = [afrm_finsight_dates, lc_finsight_dates, oprt_finsight_dates, sofi_finsight_dates, upst_finsight_dates]

afrm_finsight_sizes = pd.read_csv('Output data/finsight/AFRM/finsight_with_stock_with_benchmark.csv')['Sum_SZEM'].values
lc_finsight_sizes = pd.read_csv('Output data/finsight/LC/finsight_with_stock_with_benchmark.csv')['Sum_SZEM'].values
oprt_finsight_sizes = pd.read_csv('Output data/finsight/OPRT/finsight_with_stock_with_benchmark.csv')['Sum_SZEM'].values
sofi_finsight_sizes = pd.read_csv('Output data/finsight/SOFI/finsight_with_stock_with_benchmark.csv')['Sum_SZEM'].values
upst_finsight_sizes = pd.read_csv('Output data/finsight/UPST/finsight_with_stock_with_benchmark.csv')['Sum_SZEM'].values
finsight_sizes = [afrm_finsight_sizes, lc_finsight_sizes, oprt_finsight_sizes, sofi_finsight_sizes, upst_finsight_sizes]





### AFRM ###



plt.plot(afrm['Date'].values, afrm['d1_Vol'].values, label = "Volatility", color ="green")
# plt.plot(afrm['Date'].values, afrm['d30_BenchVol'].values, label ="BenchVol", color ="grey")
ax2 = plt.twinx()
ax2.plot(afrm['Date'].values, afrm['Adj Close'].values, label = "BenchVol", color ="grey")
# plt.plot(afrm['Date'].values, afrm['adj_1_change'].values, label ="BenchVol", color ="grey")
plt.title('Affirm Volatility and ABS issuance')
plt.ylabel('Volatility')

# for i in abs_report_dates:
#     plt.axvline(x=f'{i}', ymin=0, ymax=1, color='grey', linestyle='--', linewidth=2)

for date, size in zip(afrm_finsight_dates, afrm_finsight_sizes):
    plt.axvline(x=f'{date}', ymin=0, ymax=1, color='r', linestyle='--', linewidth=1)
    plt.text(x=f'{date}', y=120, s = f'${int(size)}M ABS issuance', rotation=90, ha='right', va='bottom', color = "r", fontsize = 12)

# formatter = mdates.DateFormatter('%m')
# plt.gca().xaxis.set_major_formatter(formatter)

plt.xticks(afrm['Date'].values[::90], afrm['Date'].values[::90])
plt.ylabel('Volatility')
ax2.set_ylabel('Adj Close')
plt.legend()
plt.show()
#
# ### LC ###
#
# plt.plot(lc['Date'].values, lc['d30_Vol'].values, label ="Volatility", color ="blue")
# plt.plot(lc['Date'].values, lc['d30_BenchVol'].values, label ="BenchVol", color ="grey")
# plt.title('lc')
# plt.ylabel('Volatility')
#
# # for i in abs_report_dates:
# #     plt.axvline(x=f'{i}', ymin=0, ymax=1, color='grey', linestyle='--', linewidth=2)
#
# for date in lc_finsight_dates_sizes:
#     plt.axvline(x=f'{date}', ymin=0, ymax=1, color='red', linestyle='--', linewidth=1)
#     # plt.text(x=f'{date}', 1.1, f'${size}M issuance', rotation=90, ha='center', va='bottom')
#
#
# plt.ylabel('Volatility')
# plt.legend()
# plt.show()
#
# ### OPRT ###
#
# plt.plot(oprt['Date'].values, oprt['d30_Vol'].values, label ="Volatility", color ="blue")
# plt.plot(oprt['Date'].values, oprt['d30_BenchVol'].values, label ="BenchVol", color ="grey")
# plt.title('oprt')
# plt.ylabel('Volatility')
#
# # for i in abs_report_dates:
# #     plt.axvline(x=f'{i}', ymin=0, ymax=1, color='grey', linestyle='--', linewidth=2)
#
# for date in oprt_finsight_dates_sizes:
#     plt.axvline(x=f'{date}', ymin=0, ymax=1, color='red', linestyle='--', linewidth=1)
#     # plt.text(x=f'{date}', 1.1, f'${size}M issuance', rotation=90, ha='center', va='bottom')
#
#
# plt.ylabel('Volatility')
# plt.legend()
# plt.show()
#
# ### SOFI ###
#
# plt.plot(sofi['Date'].values, sofi['d30_Vol'].values, label ="Volatility", color ="blue")
# plt.plot(sofi['Date'].values, sofi['d30_BenchVol'].values, label ="BenchVol", color ="grey")
# plt.title('sofi')
# plt.ylabel('Volatility')
#
# # for i in abs_report_dates:
# #     plt.axvline(x=f'{i}', ymin=0, ymax=1, color='grey', linestyle='--', linewidth=2)
#
# for date in sofi_finsight_dates_sizes:
#     plt.axvline(x=f'{date}', ymin=0, ymax=1, color='red', linestyle='--', linewidth=1)
#     # plt.text(x=f'{date}', 1.1, f'${size}M issuance', rotation=90, ha='center', va='bottom')
#
#
# plt.ylabel('Volatility')
# plt.legend()
# plt.show()
#
# ### UPST ###
#
# plt.plot(upst['Date'].values, upst['d30_Vol'].values, label ="Volatility", color ="blue")
# plt.plot(upst['Date'].values, upst['d30_BenchVol'].values, label ="BenchVol", color ="grey")
# plt.title('upst')
# plt.ylabel('Volatility')
#
# # for i in abs_report_dates:
# #     plt.axvline(x=f'{i}', ymin=0, ymax=1, color='grey', linestyle='--', linewidth=2)
#
# for date in upst_finsight_dates_sizes:
#     plt.axvline(x=f'{date}', ymin=0, ymax=1, color='red', linestyle='--', linewidth=1)
#     # plt.text(x=f'{date}', 1.1, f'${size}M issuance', rotation=90, ha='center', va='bottom')
#
#
# plt.ylabel('Volatility')
# plt.legend()
# plt.show()