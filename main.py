# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import pandas
from datetime import datetime

file_name = "AFRM20Z1_20221011.xlsx - AFRM20Z1-HistInfo"
full_month_format = "%b %d, %Y"

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
    test= df.loc[['1mo CPR','Life CPR']]

    df2 = test.T
    df2 = df2.drop("Unnamed: 1")
    df2['1mo CPR'] = df2['1mo CPR'].replace(['-'], '0.0')
    df2['1mo CPR'] = df2['1mo CPR'].astype(float)
    df2['Life CPR'] = df2['Life CPR'].replace(['-'], '0.0')
    df2['Life CPR'] = df2['Life CPR'].astype(float)

    df2['spread'] = df2['1mo CPR']-df2['Life CPR']
    #df2.set_index(df.columns[0])
    df2.to_csv(str(file_name+'_reformatted.csv'))

    ###### Stock file ######
    file_name = "AFRM20Z1_20221011.xlsx - AFRM20Z1-HistInfo" + '_reformatted.csv'
    file_name_stock = "AFRM"
    # merge the 2 files on the date column
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

    result = df2.join(test)
    result = pandas.merge(df2, test, left_index=True, right_index=True, how='outer')

    print('end')


