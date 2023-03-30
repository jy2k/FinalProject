import matplotlib.pyplot as plt
import pandas as pd

### Gather all stock data ###

afrm = pd.read_csv('stocks source data/AFRM.csv')
lc = pd.read_csv('stocks source data/LC.csv')
oprt = pd.read_csv('stocks source data/OPRT.csv')
sofi = pd.read_csv('stocks source data/SOFI.csv')
upst = pd.read_csv('stocks source data/UPST.csv')
all_stock_data=[afrm, lc, oprt, sofi, upst]

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

list_of_company_names = ['Affirm', 'Lending Club', 'Oportun', 'SoFi', 'Upstart']


def export_vol_close_abss_company_graph(company_stock_df, company_fin_dates, company_fin_sizes, company_name):
    print(f'Here is the graph for {company_name}')
    plt.plot(company_stock_df['Date'].values, company_stock_df['d1_Vol'].values, label="Volatility", color="green")
    plt.title(f'{company_name} Stock, Volatility and ABS issuance over time')
    plt.xticks(company_stock_df['Date'].values[::90], company_stock_df['Date'].values[::90])
    plt.ylabel('Volatility')
    ax2 = plt.twinx()
    ax2.plot(company_stock_df['Date'].values, company_stock_df['Adj Close'].values, label="Adj Close", color="grey")
    plt.plot(company_stock_df['Date'].values, company_stock_df['d1_Vol'].values, label="Volatility", color="green")
    plt.xticks(company_stock_df['Date'].values[::66], company_stock_df['Date'].values[::66])
    ax2.set_ylabel('Adj Close')

    for date, size in zip(company_fin_dates, company_fin_sizes):
        plt.axvline(x=f'{date}', ymin=0, ymax=1, color='r', linestyle='--', linewidth=1)
        plt.text(x=f'{date}', y=(sum(company_stock_df['Adj Close'].values)/len(company_stock_df['Adj Close'].values)), s=f'${int(size)}M ABS issuance', rotation=90, ha='right', va='bottom', color="r",
                 fontsize=8)

    plt.legend()
    plt.show()

for company, fin_dates, fin_sizes, name in zip (all_stock_data,finsight_dates,finsight_sizes, list_of_company_names):
    export_vol_close_abss_company_graph(company, fin_dates, fin_sizes, name)