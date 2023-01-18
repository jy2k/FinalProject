# This file takes cohort files of each stock
# filters out the required columns (list_of_params)
# takes the stock data from step 1 and filters out the required columns (stock_column_names)
# it then merges for each stock both data sources (stock and cohort)
# In the end it save each cohort+stock under "Output data/Cohort stock/{stock}/file_{i}_benchmark.csv"
import pandas
from datetime import datetime

###### Params ######
# https://www.programiz.com/python-programming/datetime/strptime
import pandas as pd

import utils

list_of_params = ['1mo CPR','Gross Coupon', 'Accum Net Loss%', 'Annualized Net Loss Rate', 'Delinq 30+', 'Number of Assets', 'Life CDR', 'Life CPR']

stock_column_names = ['Open','High','Low','Close','Adj Close','Volume','adj_1','adj_7','adj_30','adj_90','adj_1_change','adj_7_change','adj_30_change','adj_90_change', 'avg_adj_1_change','avg_adj_7_change','avg_adj_30_change','avg_adj_90_change', 'd1_Vol', 'd7_Vol' ,'d30_Vol', 'd90_Vol','d1_BenchVol','d7_BenchVol','d30_BenchVol','d90_BenchVol','d1_ExcessVol','d7_ExcessVol','d30_ExcessVol','d90_ExcessVol']

list_of_affirm_cohort = ['Cohort source data/AFRM/20-1/AFRM20Z1_20221011.xlsx - AFRM20Z1-HistInfo.csv',
                         'Cohort source data/AFRM/20-2/AFRM20Z2_20221011.xlsx - AFRM20Z2-HistInfo.csv',
                         'Cohort source data/AFRM/21-1/AFRM21A_20221011.xlsx - AFRM21A-HistInfo.csv'] # no accum net loss %

list_of_lendingclub_cohort = ['Cohort source data/LC/19-1/LCR191_20220928.xlsx - LCR191-CStats.csv',
                         'Cohort source data/LC/20-1/LCR201_20220928(2).xlsx - LCR201-CStats.csv',
                         'Cohort source data/LC/21-1/LCLC21N1_20220928.xlsx - LCLC21N1-CStats.csv']

list_of_oportun_cohort = ['Cohort source data/OPRT/19-1/OPF1319A_20221011.xlsx - OPF1319A-HistInfo.csv',
                         'Cohort source data/OPRT/20-1/OPF2001_20221011.xlsx - OPF2001-HistInfo.csv', # ['Gross Coupon', 'Number of Assets'] not in index
                         'Cohort source data/OPRT/21-1/OPF21A_20221011.xlsx - OPF21A-HistInfo.csv']

list_of_sofi_cohort = ['Cohort source data/SOFI/19-4/SFLP1904_20221011.xlsx - SFLP1904-HistInfo.csv',
                         'Cohort source data/SOFI/20-1/SFLP2001_20221011.xlsx - SFLP2001-HistInfo.csv',
                         'Cohort source data/SOFI/21-1/SFLP2101_20221011.xlsx - SFLP2101-HistInfo.csv']

list_of_upst_cohort = ['Cohort source data/UPST/20-1/UPSP20S1_20220928.xlsx - UPSP20S1-CStats.csv',
                         'Cohort source data/UPST/21-1/UPSP2110_20220928.xlsx - UPSP2110-CStats.csv',
                         'Cohort source data/UPST/22-1P/UPSP22P1_20220928.xlsx - UPSP22P1-CStats.csv',
                         'Cohort source data/UPST/22-1S/UPSP22S1_20220928.xlsx - UPSP22S1-CStats.csv']

dict_cohort_files = {'AFRM': {'files_cohort' : list_of_affirm_cohort, 'date_format' : "%b %d, %Y", 'day_of_the_month' : 15},
                         'LC': { 'files_cohort' : list_of_lendingclub_cohort, 'date_format' : "%b %y", 'day_of_the_month' : 1},
                        'OPRT': { 'files_cohort' : list_of_oportun_cohort, 'date_format' : "%b %d, %Y", 'day_of_the_month' : 8},
                        'SOFI': { 'files_cohort' : list_of_sofi_cohort, 'date_format' : "%b %d, %Y", 'day_of_the_month' : 25},
                        'UPST': { 'files_cohort' : list_of_upst_cohort, 'date_format' : "%b %y", 'day_of_the_month' : 1}}


def work(filename, stock, date_format, day_of_the_month,column_params):

    ###### Cohort file ######
    df_cohort = pandas.read_csv(filename, index_col=0)
    df_cohort.index.astype(str, copy=False)

    #Get Deal name
    deal = df_cohort.loc['WALA','Graph']
    print(deal)

    #Change column name to camel case
    for val in df_cohort.columns:
        if(val != 'Unnamed: 1' and val !='Graph' and val !='Prepay Group'):
            print(val)
            new_format = datetime.strptime(val, date_format)
            df_cohort = df_cohort.rename(columns={val: new_format})

    print(str('working on: '+ filename))
    #Select specific columns
    df_cohort = df_cohort.loc[column_params]
    df_cohort = df_cohort[~df_cohort.index.duplicated(keep='first')]

    try: df_cohort = df_cohort.drop("Graph", axis=1)
    except: print("Graph does not exist")

    #Transpose
    df_cohort = df_cohort.T

    try: df_cohort = df_cohort.drop("Unnamed: 1")
    except: print("unnamed: 1 does not exist")

    #Change format to float
    #Replace missing values
    for param in column_params:
        df_cohort[param] = df_cohort[param].replace(['-'], '0.0')
        df_cohort[param] = df_cohort[param].astype(str).str.replace(',', '')
        df_cohort[param] = df_cohort[param].astype(float)

    df_cohort['1mo CPR'] = df_cohort['1mo CPR'].astype("string")
    df_cohort['1mo CPR'] = deal

    ###### Stock file ######

    df = pandas.read_csv(f'stocks source data/{stock}.csv')

    import utils
    df_stock_filtered_final = utils.filter_date(df, day_of_the_month)

    df_cohort_stock = pandas.merge(df_cohort, df_stock_filtered_final, left_index=True, right_index=True, how='outer')
    #df_cohort_stock.drop(df_cohort_stock.columns[df.columns.str.contains('Unnamed', case=False)], axis=1, inplace=True)
    df_cohort_stock.drop(df_cohort_stock.columns[df_cohort_stock.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)

    df_cohort_stock.columns = column_params + stock_column_names
    df_cohort_stock.index.name = 'Date'

    df_cohort_stock = df_cohort_stock.dropna()

    return df_cohort_stock

for stock,value in dict_cohort_files.items():
    print(value)
    i=0
    for file in value['files_cohort']:
        print(file)
        current_day_of_the_month = value['day_of_the_month']

        if file == 'Cohort source data/AFRM/21-1/AFRM21A_20221011.xlsx - AFRM21A-HistInfo.csv':
            current_list = ['1mo CPR','Gross Coupon', 'Annualized Net Loss Rate', 'Delinq 30+', 'Number of Assets', 'Life CDR']
        elif file ==  'Cohort source data/OPRT/20-1/OPF2001_20221011.xlsx - OPF2001-HistInfo.csv':
            current_day_of_the_month = 15
        else:
            current_list = list_of_params
        if 'OPRT' in file:
            current_list = ['1mo CPR','Gross Coupon (Derived)', 'Annualized Net Loss Rate', 'Delinq 30+', 'Life CDR']

        df_cohort_stock = work(stock=stock, filename=file, day_of_the_month=current_day_of_the_month, date_format=value['date_format'], column_params=current_list)
        #df_cohort_stock.drop('Date', axis=1, inplace=True)
        ## adding the benchmark-clean.csv to the df_cohort_stock
        df_cohort_stock.to_csv(f'Output data/Cohort stock/{stock}/file_{i}.csv')
        df_cohort_stock = df_cohort_stock.reset_index()
        df_cohort_stock['Date'] = df_cohort_stock['Date'].astype('datetime64[ns]')

        df_benchmark_clean = pd.read_csv('Output data/benchmark-clean.csv')
        df_benchmark_clean['Date'] = df_benchmark_clean['Date'].astype('datetime64[ns]')
        df_benchmark_clean.set_index('Date')
        df_benchmark_clean_dropped_na = df_benchmark_clean.dropna()
        df_benchmark_clean_filtered = utils.filter_date(data=df_benchmark_clean_dropped_na, day_of_the_month=current_day_of_the_month)
        df_benchmark_clean_filtered.reset_index(inplace=True)
        df_cohort_stock_bencharmark = df_cohort_stock.merge(df_benchmark_clean_filtered, how='left', left_on='Date', right_on='index')
        df_cohort_stock_bencharmark.to_csv(f'Output data/Cohort stock/{stock}/file_{i}_benchmark.csv')
        i+=1
