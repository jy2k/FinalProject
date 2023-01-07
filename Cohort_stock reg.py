import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
import pandas as pd

def add_columns(df):
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.str.replace('+', '')
    df['Gross_Coupon_Minus_Annualized_Net_Loss_Rate'] = df['Gross_Coupon'].subtract(df['Annualized_Net_Loss_Rate'])
    df['d1_dist_from_bench'] = df['adj_1_change'] - df['avg_adj_1_change']
    df['d7_dist_from_bench'] = df['adj_7_change'] - df['avg_adj_7_change']
    df['d30_dist_from_bench'] = df['adj_30_change'] - df['avg_adj_30_change']
    df['d90_dist_from_bench'] = df['adj_90_change'] - df['avg_adj_90_change']
    return df

def my_ols(df, X_list, y_list, use_adj=False, test_percent=0.2):

    in_sample_r2 = []
    out_of_sample_r2 = []

    for i in y_list:
        y = df[i]
        X = df[X_list]
        train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=test_percent)
        results = sm.OLS(train_y, train_X).fit()
        from sklearn.metrics import r2_score
        ypred = results.predict(test_X)
        r2 = r2_score(test_y, ypred)
        #print(f'R2: {r2}')
        #print(results.summary())

        out_of_sample_r2.append(r2)
        in_sample_r2.append(results.rsquared_adj if use_adj else results.rsquared)

    print('In of sample: ')
    print(in_sample_r2)
    print('Out of sample: ')
    print(out_of_sample_r2)

    return in_sample_r2, out_of_sample_r2

def plot_r2(r2_change_list, r2_bench_list):
    x = ['1d', '7d', '30d', '90d']

    plt.plot(x, r2_change_list, label ="stock change", color ="blue")
    plt.plot(x, r2_bench_list, label ="Benchmark", color ="green")
    plt.title('AFRM R^2 for % change and Benchmark in stock')
    plt.ylabel('R^2')
    plt.grid()
    plt.legend()
    plt.show()


##################### Run Regression #####################

afrm_cohort_stock1 = pd.read_csv(f'Output data/cohort stock/AFRM/file_0_benchmark.csv')
afrm_cohort_stock2 = pd.read_csv(f'Output data/cohort stock/AFRM/file_1_benchmark.csv')
afrm_cohort_stock3 = pd.read_csv(f'Output data/cohort stock/AFRM/file_2_benchmark.csv')
afrm_files = [afrm_cohort_stock1, afrm_cohort_stock2, afrm_cohort_stock3]

lc_cohort_stock1 = pd.read_csv(f'Output data/cohort stock/LC/file_0_benchmark.csv')
lc_cohort_stock2 = pd.read_csv(f'Output data/cohort stock/LC/file_1_benchmark.csv')
lc_cohort_stock3 = pd.read_csv(f'Output data/cohort stock/LC/file_2_benchmark.csv')
lc_files = [lc_cohort_stock1,lc_cohort_stock3] # lc_cohort_stock2

oprt_cohort_stock1 = pd.read_csv(f'Output data/cohort stock/OPRT/file_0_benchmark.csv')
oprt_cohort_stock2 = pd.read_csv(f'Output data/cohort stock/OPRT/file_1_benchmark.csv')
oprt_cohort_stock3 = pd.read_csv(f'Output data/cohort stock/OPRT/file_2_benchmark.csv')
oprt_files = [oprt_cohort_stock1, oprt_cohort_stock3] #oprt_cohort_stock2

sofi_cohort_stock1 = pd.read_csv(f'Output data/cohort stock/SOFI/file_0_benchmark.csv')
sofi_cohort_stock2 = pd.read_csv(f'Output data/cohort stock/SOFI/file_1_benchmark.csv')
sofi_cohort_stock3 = pd.read_csv(f'Output data/cohort stock/SOFI/file_2_benchmark.csv')
sofi_files = [sofi_cohort_stock1, sofi_cohort_stock3] # lc_cohort_stock2

upst_cohort_stock1 = pd.read_csv(f'Output data/cohort stock/UPST/file_0_benchmark.csv')
upst_cohort_stock2 = pd.read_csv(f'Output data/cohort stock/UPST/file_1_benchmark.csv')
upst_cohort_stock3 = pd.read_csv(f'Output data/cohort stock/UPST/file_2_benchmark.csv')
upst_cohort_stock4 = pd.read_csv(f'Output data/cohort stock/UPST/file_2_benchmark.csv')
upst_files = [upst_cohort_stock1, upst_cohort_stock2, upst_cohort_stock3, upst_cohort_stock4]

import itertools
combined_cohort_deals = list(itertools.chain(afrm_files, lc_files, oprt_files, sofi_files, upst_files))

#### Regression runs
df_combined_files = pd.concat(combined_cohort_deals, ignore_index=True, sort=False)
df_combined_files = add_columns(df_combined_files)

print('working on adj change')
y_list = ['d1_dist_from_bench', 'd7_dist_from_bench', 'd30_dist_from_bench', 'd90_dist_from_bench']
X_list = ['Annualized_Net_Loss_Rate', 'Life_CDR']
bench_in_sample_r2, out_of_sample_r2 = my_ols(df=df_combined_files, X_list=X_list, y_list=y_list)

print('working on adj change')
y_list = ['adj_1_change', 'adj_7_change', 'adj_30_change', 'adj_90_change']
X_list = ['Annualized_Net_Loss_Rate', 'Life_CDR']
in_sample_r2, out_of_sample_r2 = my_ols(df=df_combined_files, X_list=X_list, y_list=y_list)

plot_r2(in_sample_r2, bench_in_sample_r2)