import pandas as pd
import statsmodels.formula.api as sm
import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels.formula.api as smf
from statsmodels.compat import lzip
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols


# COMPANIES = []
# Start_date = ''
# End_date = ''
#
# df = pd.DataFrame({'c1': [10, 11, 12], 'c2': [100, 110, 120]})
# df = df.reset_index()  # make sure indexes pair with number of rows
#
# for index, row in df.iterrows():
#     print(row['c1'], row['c2'])
#
# my_list = {'AFRM_adj_1_change_pred': 'AFRM_adj_1_change',
#                     'UPST_adj_1_change_pred': 'UPST_adj_1_change',
#                     'LC_adj_1_change_pred': 'LC_adj_1_change',
#                     'SOFI_adj_1_change_pred': 'SOFI_adj_1_change',
#                     'OPRT_adj_1_change_pred': 'OPRT_adj_1_change'}


## Trade strat

### Step 1 - Get 1d predictions for each stock + stock data
# + add long_gain and short_gain columns


### Step 2 - Sort the predictions

### Step 3 - choose the largest 2 and smallest 2

### Step 4 - Multiple largest two by 1 and smallest two by -1

### Step 5 -

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
#at this point the DAtaframe is ready
#now need to fill in each long_gain and short_gain prediction

for index, row in df.iterrows():
    #print(index, row['Date'], row['AFRM_adj_1_change'], row['AFRM_adj_1_change_pred'])
    #Create a dictionary from the row
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
    df.at[index, 'long_gain'] = 0.5 * (actual[max_key[:-5]])
    df.at[index, 'short_gain'] = -0.5 * (actual[min_key[:-5]])

    df.at[index, 'daily_return'] = df.at[index, 'long_gain'] + df.at[index, 'short_gain']

    print('test')

print('end')












