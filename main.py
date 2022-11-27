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

    df = pandas.read_csv("AFRM20Z1_20221011.xlsx - AFRM20Z1-HistInfo.csv", index_col=0)
    df.index.astype(str, copy=False)
    print(df.columns)
    #df = df.rename_axis(["sdfsdd","Sdfdsfs","Sep 15, 2022","Aug 15, 2022","Jul 15, 2022","Jun 15, 2022","May 15, 2022","Apr 15, 2022","Mar 15, 2022","Feb 15, 2022","Jan 15, 2022","Dec 15, 2021","Nov 15, 2021","Oct 15, 2021","Sep 15, 2021","Aug 15, 2021","Jul 15, 2021","Jun 15, 2021","May 15, 2021","Apr 15, 2021","Mar 15, 2021","Feb 15, 2021","Jan 15, 2021","Dec 15, 2020","Nov 15, 2020","Oct 15, 2020","Sep 15, 2020","Jul 01, 2020"]).reset_index()
    for val in df.columns:
        df = df.rename(columns={val: 'test'})

    #df2 = df.rename(index={'Sep 15, 2022': 'Index_3'}, inplace=True)

    print(df.loc['1mo CPR'])
    #df.index.name = 'test'
    #print(df.index.name)
    #df.set_index(0)
    #df = df.query('test == 1mo CPR')
    test= df.loc[['1mo CPR','Life CPR']]
    #print(df.columns)
    #df2 = pandas.DataFrame(data=test)
    df2 = test.T
    df2['1mo CPR'] = df2['1mo CPR'].replace(['-'], '0.0')
    df2['1mo CPR'] = df2['1mo CPR'].astype(float)
    df2['Life CPR'] = df2['Life CPR'].replace(['-'], '0.0')
    df2['Life CPR'] = df2['Life CPR'].astype(float)

    df2['spread'] = df2['1mo CPR']-df2['Life CPR']

    print('end')


