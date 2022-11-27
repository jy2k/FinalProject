# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import pandas
from datetime import datetime

file_name = "AFRM20Z1_20221011.xlsx - AFRM20Z1-HistInfo.csv"
full_month_format = "%b %d, %Y"

if __name__ == '__main__':

    df = pandas.read_csv(file_name, index_col=0)
    df.index.astype(str, copy=False)

    for val in df.columns:
        if(val != 'Unnamed: 1'):
            interim = datetime.strptime(val, full_month_format)
            month = str(interim.month)
            year = str(interim.year)
            new_format = str(month + '/' + year)
            df = df.rename(columns={val: new_format})

    #select specific columns
    test= df.loc[['1mo CPR','Life CPR']]

    df2 = test.T
    df2['1mo CPR'] = df2['1mo CPR'].replace(['-'], '0.0')
    df2['1mo CPR'] = df2['1mo CPR'].astype(float)
    df2['Life CPR'] = df2['Life CPR'].replace(['-'], '0.0')
    df2['Life CPR'] = df2['Life CPR'].astype(float)

    df2['spread'] = df2['1mo CPR']-df2['Life CPR']

    print('end')


