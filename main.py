import pandas
from datetime import datetime

###### Params ######

file_1 = "AFRM20Z1_20221011.xlsx - AFRM20Z1-HistInfo"
full_month_format_file_1 = "%b %y"

file_2 = "stocks/LC"
full_month_format_file_2 = "%Y-%m-%d"

file_3 = "Finsight data - Affirm_edited"
full_month_format_file_3 = "%B %d, %Y"

list_of_params = ['1mo CPR','Gross Coupon', 'Accum Net Loss%', 'Annualized Net Loss Rate', 'Delinq 30+', 'Number of Assets', 'Life CDR', 'Life CPR']
columns_names = ['Deal','Gross_Coupon','Accum_Net_Loss_precent','Annualized_Net_Loss_Rate','Delinq_30','Number_of_Assets','Life_CDR','Life_CPR','Gross_Coupon_Accum_Net_Loss_precent','Num_Assets_in_Delinq_30_Days_Number_of_Assets','Open','High','Low','Close','Adj_Close','Volume']

list_of_affirm_cohort = ['cohort/Affirm/20-1/AFRM20Z1_20221011.xlsx - AFRM20Z1-HistInfo.csv',
                         'cohort/Affirm/20-2/AFRM20Z2_20221011.xlsx - AFRM20Z2-HistInfo.csv',
                         'cohort/Affirm/21-1/AFRM21A_20221011.xlsx - AFRM21A-HistInfo.csv']

list_of_lendingclub_cohort = ['cohort/LendingClub/19-1/LCR191_20220928.xlsx - LCR191-CStats.csv',
                         'cohort/LendingClub/20-1/LCR201_20220928(2).xlsx - LCR201-CStats.csv',
                         'cohort/LendingClub/21-1/LCLC21N1_20220928.xlsx - LCLC21N1-CStats.csv']
###### Functions ######

def concat_csvs(list_csvs):
    df_full = pandas.DataFrame()

    for csv in list_csvs:
        current = pandas.read_csv(csv, index_col=0)
        df_full = df_full.append(current)

    return df_full

def bucketize_date(val, full_month_format):
    interim = datetime.strptime(val, full_month_format)
    month = str(interim.month)
    year = str(interim.year)
    new_format = str(month + '/' + year)
    return new_format

if __name__ == '__main__':

    ###### Cohort file ######
    df_cohort = pandas.read_csv(list_of_lendingclub_cohort[2], index_col=0)

    df_cohort.index.astype(str, copy=False)
    deal = df_cohort.loc['WALA','Graph']

    print(deal)
    for val in df_cohort.columns:
        if(val != 'Unnamed: 1' and val !='Graph' and val !='Prepay Group'):
            new_format = datetime.strptime(val, full_month_format_file_1)
            df_cohort = df_cohort.rename(columns={val: new_format})

    #select specific columns
    df_cohort = df_cohort.loc[list_of_params]
    df_cohort = df_cohort[~df_cohort.index.duplicated(keep='first')]
    try:
        df_cohort = df_cohort.drop("Graph", axis=1)
    except:
        print("Graph does not exist")

    df_cohort = df_cohort.T

    try:
        df_cohort = df_cohort.drop("Unnamed: 1")
    except:
        print("unnamed: 1 does not exist")


    for param in list_of_params:
        df_cohort[param] = df_cohort[param].replace(['-'], '0.0')
        df_cohort[param] = df_cohort[param].str.replace(',', '')
        df_cohort[param] = df_cohort[param].astype(float)

    df_cohort['1mo CPR'] = df_cohort['1mo CPR'].astype("string")
    df_cohort['1mo CPR'] = deal

    df_cohort['Gross Coupon - Accum Net Loss%'] = df_cohort['Gross Coupon'] - df_cohort['Accum Net Loss%']
    df_cohort['Num Assets in Delinq 30+ Days / Number of Assets'] = df_cohort['Delinq 30+'] / df_cohort['Number of Assets']

    #df_cohort.to_csv(str(file_1+'_reformatted.csv'))

    ###### Stock file ######

    df = pandas.read_csv(str(file_2 + '.csv'))

    df.loc[:, 'Date'] = pandas.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df_stock_filtered_final = df.resample('SMS').first()
    #df_resampled['day_of_month'] = df_resampled.index.day
    #df_stock_filtered_final = df_resampled[df_resampled.day_of_month.eq(15)]

    df_cohort_stock = pandas.merge(df_cohort, df_stock_filtered_final, left_index=True, right_index=True, how='outer')
    #df_cohort_stock.drop('day_of_month', axis=1, inplace=True)
    df_cohort_stock.columns

    df_cohort_stock.columns = columns_names
    df_cohort_stock.index.name = 'Date'
    df_cohort_stock['series'] = 1

    df_cohort_stock = df_cohort_stock.dropna()

    df_cohort_stock.to_csv('file3.csv')

    print('end')


