# This script takes the stock+cohort data
# Trains a model (currently xgboost but see instructions below on how to change line 67)
# creates prediction files and saves for each stock in stock+'_preds.csv' file
import pandas as pd
from sklearn.model_selection import train_test_split
#https://medium.com/@polanitzer/the-minimum-mean-absolute-error-mae-challenge-928dc081f031


afrm_files = [pd.read_csv(f'Output data/cohort stock/AFRM/file_0_benchmark.csv'),
              pd.read_csv(f'Output data/cohort stock/AFRM/file_1_benchmark.csv'),
              pd.read_csv(f'Output data/cohort stock/AFRM/file_2_benchmark.csv')]

lc_files = [pd.read_csv(f'Output data/cohort stock/LC/file_0_benchmark.csv'),
              pd.read_csv(f'Output data/cohort stock/LC/file_1_benchmark.csv'),
              pd.read_csv(f'Output data/cohort stock/LC/file_2_benchmark.csv')]

oprt_files = [pd.read_csv(f'Output data/cohort stock/OPRT/file_0_benchmark.csv'),
              pd.read_csv(f'Output data/cohort stock/OPRT/file_1_benchmark.csv'),
              pd.read_csv(f'Output data/cohort stock/OPRT/file_2_benchmark.csv')]

sofi_files = [pd.read_csv(f'Output data/cohort stock/SOFI/file_0_benchmark.csv'),
              pd.read_csv(f'Output data/cohort stock/SOFI/file_1_benchmark.csv'),
              pd.read_csv(f'Output data/cohort stock/SOFI/file_2_benchmark.csv')]

upst_files = [pd.read_csv(f'Output data/cohort stock/UPST/file_0_benchmark.csv'),
              pd.read_csv(f'Output data/cohort stock/UPST/file_1_benchmark.csv'),
              pd.read_csv(f'Output data/cohort stock/UPST/file_2_benchmark.csv'),
              pd.read_csv(f'Output data/cohort stock/UPST/file_3_benchmark.csv')]

dict_of_stock_files = {'AFRM': afrm_files,
                          'LC': lc_files,
                          'OPRT': oprt_files,
                          'SOFI': sofi_files,
                          'UPST': upst_files}

def add_columns_with_predictions(stock, model, pred_column, dates_df, X):
    #Load specific stock file
    y_pred = model.predict(X)

    df = pd.DataFrame()
    df['Date'] = dates_df['Date']
    df[str(stock+'_'+pred_column+'_'+'pred')] = y_pred
    df.to_csv(str(stock+'_preds.csv'))

def add_columns(df):
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.str.replace('+', '')
    try:
        df['Gross_Coupon_Minus_Annualized_Net_Loss_Rate'] = df['Gross_Coupon'].subtract(df['Annualized_Net_Loss_Rate'])
    except:
        df['Gross_Coupon_Minus_Annualized_Net_Loss_Rate'] = df['Gross_Coupon_(Derived)'].subtract(df['Annualized_Net_Loss_Rate'])
    df['d1_dist_from_bench'] = df['adj_1_change'] - df['avg_adj_1_change']
    df['d7_dist_from_bench'] = df['adj_7_change'] - df['avg_adj_7_change']
    df['d30_dist_from_bench'] = df['adj_30_change'] - df['avg_adj_30_change']
    df['d90_dist_from_bench'] = df['adj_90_change'] - df['avg_adj_90_change']
    return df

def run_model(stock, dataset, pred_column):
    interim = pd.DataFrame(columns=['Model', pred_column])
    y = dataset[pred_column].astype('float')
    if stock == 'OPRT':
        X = dataset[['Annualized_Net_Loss_Rate', 'Life_CDR', 'Gross_Coupon_Minus_Annualized_Net_Loss_Rate']].astype('float')
    else:
        X = dataset[['Annualized_Net_Loss_Rate', 'Life_CDR', 'Life_CPR', 'Gross_Coupon_Minus_Annualized_Net_Loss_Rate']].astype('float')

    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.1)

    ## THIS IS WHERE THE MODEL TRAINNING HAPPENS ##
    # switch the following 3 lines from a different model.
    # The models are in "additional models.py" file
    from sklearn.ensemble import RandomForestRegressor
    rf = RandomForestRegressor(random_state=42, n_estimators=100)
    rf.fit(train_X, train_y)
    print('feature importance: ')
    print(str(rf.feature_names_in_))
    print(str(rf.feature_importances_))


    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_absolute_error

    linreg = LinearRegression()
    linreg.fit(train_X, train_y)
    ypred = linreg.predict(test_X)
    l1 = mean_absolute_error(test_y, ypred)
    print(f'{stock} Mean Linear regression MAE: %.3f' % l1)

    import statsmodels.formula.api as smf
    new_df = train_X
    new_df[pred_column] = train_y
    if stock == 'OPRT':
        results = smf.ols(f'{pred_column} ~ Annualized_Net_Loss_Rate + Life_CDR + Gross_Coupon_Minus_Annualized_Net_Loss_Rate', data=new_df).fit()
    else:
        results = smf.ols(f'{pred_column} ~ Annualized_Net_Loss_Rate + Life_CDR + Life_CPR + Gross_Coupon_Minus_Annualized_Net_Loss_Rate', data=new_df).fit()

    print(f'{stock}:\n' + str(results.summary()))
    add_columns_with_predictions(stock, rf,pred_column, dataset[['Date']], X)

    return interim


# results = run_model('adj_1_change')
# results = results.drop('adj_1_change', axis=1)
mega_dataset = pd.DataFrame()

for stock , files in dict_of_stock_files.items():

    dataset = pd.concat(files, ignore_index=True, sort=False)

    frames = [mega_dataset, dataset]
    mega_dataset = pd.concat(frames, ignore_index=True, sort=False)

    dataset['Date'] = pd.to_datetime(dataset['Date'])
    grouped = dataset.groupby(dataset['Date'])
    # Calculate the average of the value column for each group
    dataset = grouped.mean()
    dataset = dataset.reset_index()
    dataset = add_columns(dataset)
    dataset.dropna(axis=0, inplace=True)

    for pred_column in ['adj_1_change']: ### The Y in our models is the string here, in this case "adj 1 change"
        interim = run_model(stock, dataset, pred_column)
        #results = results.merge(interim, left_on='Model', right_on='Model')


#handle the megaDataset
print('Mega dataset')
mega_dataset['Date'] = pd.to_datetime(mega_dataset['Date'])
grouped = mega_dataset.groupby(mega_dataset['Date'])
# Calculate the average of the value column for each group
mega_dataset = grouped.mean()
mega_dataset = mega_dataset.reset_index()
mega_dataset = add_columns(mega_dataset)
mega_dataset.dropna(axis=0, inplace=True)
run_model('mega', mega_dataset, 'adj_1_change')
print('end')
# print(results)
#
# import seaborn as sns
# import matplotlib.pyplot as plt
# plt.figure(figsize=(8, 8))
# sns.barplot(x='adj_7_change', y='Model', data=results)
# plt.show()