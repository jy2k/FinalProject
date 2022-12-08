import pandas
from datetime import datetime

###### Params ######
# https://www.programiz.com/python-programming/datetime/strptime

list_of_params = ['1mo CPR','Gross Coupon', 'Accum Net Loss%', 'Annualized Net Loss Rate', 'Delinq 30+', 'Number of Assets', 'Life CDR', 'Life CPR']
stock_column_names = ['Open','High','Low','Close','Adj_Close','Volume']

list_of_affirm_cohort = ['cohort/AFRM/20-1/AFRM20Z1_20221011.xlsx - AFRM20Z1-HistInfo.csv',
                         'cohort/AFRM/20-2/AFRM20Z2_20221011.xlsx - AFRM20Z2-HistInfo.csv',
                         'cohort/AFRM/21-1/AFRM21A_20221011.xlsx - AFRM21A-HistInfo.csv'] # no accum net loss %

list_of_lendingclub_cohort = ['cohort/LC/19-1/LCR191_20220928.xlsx - LCR191-CStats.csv',
                         'cohort/LC/20-1/LCR201_20220928(2).xlsx - LCR201-CStats.csv',
                         'cohort/LC/21-1/LCLC21N1_20220928.xlsx - LCLC21N1-CStats.csv']

list_of_oportun_cohort = ['cohort/OPRT/19-1/OPF1319A_20221011.xlsx - OPF1319A-HistInfo.csv',
                         'cohort/OPRT/20-1/OPF2001_20221011.xlsx - OPF2001-HistInfo.csv', # ['Gross Coupon', 'Number of Assets'] not in index
                         'cohort/OPRT/21-1/OPF21A_20221011.xlsx - OPF21A-HistInfo.csv']

list_of_sofi_cohort = ['cohort/SOFI/19-4/SFLP1904_20221011.xlsx - SFLP1904-HistInfo.csv',
                         'cohort/SOFI/20-1/SFLP2001_20221011.xlsx - SFLP2001-HistInfo.csv',
                         'cohort/SOFI/21-1/SFLP2101_20221011.xlsx - SFLP2101-HistInfo.csv']

list_of_upst_cohort = ['cohort/UPST/20-1/UPSP20S1_20220928.xlsx - UPSP20S1-CStats.csv',
                         'cohort/UPST/21-1/UPSP2110_20220928.xlsx - UPSP2110-CStats.csv',
                         'cohort/UPST/22-1P/UPSP22P1_20220928.xlsx - UPSP22P1-CStats.csv',
                         'cohort/UPST/22-1S/UPSP22S1_20220928.xlsx - UPSP22S1-CStats.csv']

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

    #df_cohort['Gross Coupon - Accum Net Loss%'] = df_cohort['Gross Coupon'] - df_cohort['Accum Net Loss%']
    #df_cohort['Num Assets in Delinq 30+ Days / Number of Assets'] = df_cohort['Delinq 30+'] / df_cohort['Number of Assets']

    #df_cohort.to_csv(str(file_1+'_reformatted.csv'))

    ###### Stock file ######

    df = pandas.read_csv(f'stocks/{stock}.csv')

    import utils
    df_stock_filtered_final = utils.filter_date(df, day_of_the_month)

    df_cohort_stock = pandas.merge(df_cohort, df_stock_filtered_final, left_index=True, right_index=True, how='outer')

    df_cohort_stock.columns = column_params+stock_column_names
    df_cohort_stock.index.name = 'Date'
    #df_cohort_stock['series'] = 1

    df_cohort_stock = df_cohort_stock.dropna()

    return df_cohort_stock

for stock,value in dict_cohort_files.items():
    print(value)
    i=0
    for file in value['files_cohort']:
        print(file)
        current_day_of_the_month = value['day_of_the_month']

        if file == 'cohort/AFRM/21-1/AFRM21A_20221011.xlsx - AFRM21A-HistInfo.csv':
            current_list = ['1mo CPR','Gross Coupon', 'Annualized Net Loss Rate', 'Delinq 30+', 'Number of Assets', 'Life CDR']
        elif file ==  'cohort/OPRT/20-1/OPF2001_20221011.xlsx - OPF2001-HistInfo.csv':
            current_list = ['1mo CPR','Gross Coupon (Derived)', 'Annualized Net Loss Rate', 'Delinq 30+', 'Life CDR']
            current_day_of_the_month = 15
        else:
            current_list = list_of_params

        df_cohort_stock = work(stock=stock, filename=file, day_of_the_month=current_day_of_the_month, date_format=value['date_format'], column_params=current_list)
        df_cohort_stock.to_csv(f'data/cohort stock/{stock}/file_{i}.csv')
        i+=1
