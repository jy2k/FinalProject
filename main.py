# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import pandas
from datetime import datetime

if __name__ == '__main__':
    full_month_date = "Sep 15, 2022"
    full_month_format = "%b %d, %Y"
    test = datetime.strptime(full_month_date, full_month_format)
    print(test.year)
    print(test.month)

    df = pandas.read_csv("AFRM20Z1_20221011.xlsx - AFRM20Z1-HistInfo.csv", index_col='Name')
    df.loc['Gross Coupon']
    #print(df.columns)
    df2 = pandas.DataFrame(data=df)
    df2 = df2.T
    df2['WALA'] = df2['WALA'].astype(float)
    df2['Accum'] = df2['Accum'].replace(['-'], '0.0')
    df2['Accum'] = df2['Accum'].astype(float)
    print('types')
    print(df2.dtypes)
    print(df2['WALA'])
    df2['spread'] = df2['WALA']-df2['Accum']

    print('end')


