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

df = pd.read_csv('/Users/eyalben-eliyahu/Desktop/mockmock.csv')
df['long_gain'] = 0
df['short_gain'] = 0

def trade (df):
    for row in df.iterrows():
        tes = row[1]['LC_adj_1_change_pred']
        my_list = [{'name': 'LC', 'pred': row[1]['LC_adj_1_change_pred'], 'actual': row[6]['LC_adj_1_change']},
                   {'name': 'UPST', 'pred': row[2]['UPST_adj_1_change_pred'], 'actual': row[7]['UPST_adj_1_change']},
                   {'name': 'SOFI', 'pred': row[3]['SOFI_adj_1_change_pred'], 'actual': row[8]['SOFI_adj_1_change']},
                   {'name': 'AFRM', 'pred': row[4]['AFRM_adj_1_change_pred'], 'actual': row[9]['AFRM_adj_1_change']},
                   {'name': 'OPRT', 'pred': row[5]['OPRT_adj_1_change_pred'], 'actual': row[10]['OPRT_adj_1_change']}]
        sorted_list = sorted(my_list, key=lambda x: x['pred'])
        df['long_gain'] = (1 * (sorted_list[0]['actual'] + sorted_list[1]['actual']))
        df['short_gain'] = (-1 * (sorted_list[4]['actual'] + sorted_list[3]['actual']))


trade(df)










