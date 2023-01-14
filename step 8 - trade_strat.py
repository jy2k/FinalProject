import pandas as pd

df = pd.read_csv('merged_file.csv')

df['AFRM_adj_1_change_pred'] = df['AFRM_adj_1_change_pred'].ffill()
df['AFRM_adj_1_change_pred'] = df['AFRM_adj_1_change_pred'].bfill()
df['UPST_adj_1_change_pred'] = df['UPST_adj_1_change_pred'].ffill()
df['UPST_adj_1_change_pred'] = df['UPST_adj_1_change_pred'].bfill()
df['SOFI_adj_1_change_pred'] = df['SOFI_adj_1_change_pred'].ffill()
df['SOFI_adj_1_change_pred'] = df['SOFI_adj_1_change_pred'].bfill()
df['LC_adj_1_change_pred'] = df['LC_adj_1_change_pred'].ffill()
df['LC_adj_1_change_pred'] = df['LC_adj_1_change_pred'].bfill()
df['OPRT_adj_1_change_pred'] = df['OPRT_adj_1_change_pred'].ffill()
df['OPRT_adj_1_change_pred'] = df['OPRT_adj_1_change_pred'].bfill()
# TODO: remove this filtering line
df = df.iloc[300:350]

df['long_gain'] = 0
df['short_gain'] = 0
df['daily_return'] = 0

for index, row in df.iterrows():

    actual = {
        'AFRM_adj_1_change': row['AFRM_adj_1_change'],

        'LC_adj_1_change': row['LC_adj_1_change'],

        'OPRT_adj_1_change': row['OPRT_adj_1_change'],

        'SOFI_adj_1_change': row['SOFI_adj_1_change'],

        'UPST_adj_1_change': row['UPST_adj_1_change'],
    }

    predicted = {
        'AFRM_adj_1_change_pred': row['AFRM_adj_1_change_pred'],

        'LC_adj_1_change_pred': row['LC_adj_1_change_pred'],

        'OPRT_adj_1_change_pred': row['OPRT_adj_1_change_pred'],

        'SOFI_adj_1_change_pred': row['SOFI_adj_1_change_pred'],

        'UPST_adj_1_change_pred': row['UPST_adj_1_change_pred'],
    }

    sorted_d = sorted(predicted.items(), key=lambda x: x[1])

    #get 2 max
    max_key = sorted_d[-1][0]
    max_2_key = sorted_d[-2][0]

    #get 2 min
    min_key = sorted_d[0][0]
    min_2_key = sorted_d[1][0]

    #creating the strat assuming weights of 0.5 -0.5
    print(index)
    df.loc[index, 'long_gain'] = 0.5 * (actual[max_key[:-5]])
    df.loc[index, 'short_gain'] = -0.5 * (actual[min_key[:-5]])

    df.loc[index, 'daily_return'] = df.loc[index, 'long_gain'] + df.loc[index, 'short_gain']

    print('end of one row iteration')

df['cumulative_returns'] = df['daily_return'].cumsum()

import matplotlib.pyplot as plt

df.plot(kind='line', x='Date', y='daily_return', title='Cummulative returns per date')
plt.show()

print('end')











