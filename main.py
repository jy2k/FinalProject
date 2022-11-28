# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import pandas
from datetime import datetime

file_name = "AFRM20Z1_20221011.xlsx - AFRM20Z1-HistInfo"
full_month_format = "%b %d, %Y"
list_of_params = ['Gross Coupon', 'Accum Net Loss%', 'Annualized Net Loss Rate', 'Delinq 30+', 'Number of Assets', 'Life CDR', 'Life CPR']

if __name__ == '__main__':

    df = pandas.read_csv(str(file_name+'.csv'), index_col=0)
    df.index.astype(str, copy=False)

    for val in df.columns:
        if(val != 'Unnamed: 1'):
            new_format = datetime.strptime(val, full_month_format)
            #interim = datetime.strptime(val, full_month_format)
            #month = str(interim.month)
            #year = str(interim.year)
            #new_format = str(month + '/' + year)
            df = df.rename(columns={val: new_format})

    #select specific columns
    test= df.loc[list_of_params]
    test2 = test[~test.index.duplicated(keep='first')]
    df2 = test2.T
    df2 = df2.drop("Unnamed: 1")

    for param in list_of_params:
        df2[param] = df2[param].replace(['-'], '0.0')
        df2[param] = df2[param].str.replace(',', '')
        df2[param] = df2[param].astype(float)

    df2['Gross Coupon - Accum Net Loss%'] = df2['Gross Coupon'] - df2['Accum Net Loss%']
    df2['Num Assets in Delinq 30+ Days / Number of Assets'] = df2['Delinq 30+'] / df2['Number of Assets']

    df2.to_csv(str(file_name+'_reformatted.csv'))

    ###### Stock file ######
    file_name = "AFRM20Z1_20221011.xlsx - AFRM20Z1-HistInfo" + '_reformatted.csv'
    file_name_stock = "AFRM"

    df3 = pandas.read_csv(str(file_name_stock + '.csv'), index_col=0)
    df3 = df3.T

    full_month_format = "%Y-%m-%d"

    for val in df3.columns:
        if (val != 'Date'):
            new_format = datetime.strptime(val, full_month_format)
            #interim = datetime.strptime(val, full_month_format)
            #month = str(interim.month)
            #year = str(interim.year)
            #new_format = str(month + '/' + year)
            df3 = df3.rename(columns={val: new_format})
    test = df3.T
    print(test.index.name)
    print(df2.index.name)

    result = pandas.merge(df2, test, left_index=True, right_index=True, how='outer')

    print('end')


