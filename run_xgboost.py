import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold
from numpy import absolute
from sklearn.metrics import mean_absolute_error
#https://medium.com/@polanitzer/the-minimum-mean-absolute-error-mae-challenge-928dc081f031

afrm_cohort_stock1 = pd.read_csv(f'Output data/cohort stock/AFRM/file_0_benchmark.csv')
afrm_cohort_stock2 = pd.read_csv(f'Output data/cohort stock/AFRM/file_1_benchmark.csv')
afrm_cohort_stock3 = pd.read_csv(f'Output data/cohort stock/AFRM/file_2_benchmark.csv')
afrm_files = [afrm_cohort_stock1, afrm_cohort_stock2, afrm_cohort_stock3]

def add_columns_with_predictions(model, pred_column, dates_df, X):
    df = pd.DataFrame()
    y_pred = model.predict(X)

    df['Date'] = dates_df['Date']
    df[str('AFRM_'+pred_column)] = y_pred
    #need to save new file
    df.to_csv('AFRM_preds.csv')
    print('success')

def add_columns(df):
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.str.replace('+', '')
    df['Gross_Coupon_Minus_Annualized_Net_Loss_Rate'] = df['Gross_Coupon'].subtract(df['Annualized_Net_Loss_Rate'])
    df['d1_dist_from_bench'] = df['adj_1_change'] - df['avg_adj_1_change']
    df['d7_dist_from_bench'] = df['adj_7_change'] - df['avg_adj_7_change']
    df['d30_dist_from_bench'] = df['adj_30_change'] - df['avg_adj_30_change']
    df['d90_dist_from_bench'] = df['adj_90_change'] - df['avg_adj_90_change']
    return df

def work(pred_column):
    interim = pd.DataFrame(columns=['Model', pred_column])
    dataset = pd.concat(afrm_files, ignore_index=True, sort=False)
    dataset = add_columns(dataset)
    dataset.dropna(axis=0, inplace=True)
    y = dataset[pred_column].astype('float')
    X = dataset[['Annualized_Net_Loss_Rate', 'Life_CDR', 'Life_CPR']].astype('float')

    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.1)

    print('XGBRegressor')

    xgbr = XGBRegressor(objective='reg:squarederror', random_state=0)
    xgbr.fit(train_X, train_y)
    ypred = xgbr.predict(test_X)
    from sklearn.model_selection import cross_val_score
    from sklearn.model_selection import RepeatedKFold
    from numpy import absolute
    cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
    # evaluate model
    scores = cross_val_score(xgbr, X, y, scoring='neg_mean_absolute_error', cv=cv, n_jobs=-1)
    # force scores to be positive
    scores = absolute(scores)
    print('Mean MAE: %.3f (%.3f)' % (scores.mean(), scores.std()) )

    list_row = ['XGBRegressor', scores.mean()]
    interim.loc[len(interim)] = list_row

    # https://scikit-learn.org/stable/modules/model_evaluation.html#r2-score-the-coefficient-of-determination
    from sklearn.metrics import r2_score
    r2 = r2_score(test_y, ypred)
    print(f'R^2: {r2}')


    print('Lasso')

    from numpy import mean
    from numpy import std
    from numpy import absolute
    from sklearn.model_selection import cross_val_score
    from sklearn.model_selection import RepeatedKFold
    from sklearn.linear_model import Lasso

    model = Lasso(alpha=0.01, random_state=0)
    # define model evaluation method
    model = model.fit(train_X, train_y)
    cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
    # evaluate model
    scores = cross_val_score(model, train_X, train_y, scoring='neg_mean_absolute_error', cv=cv, n_jobs=-1)
    # force scores to be positive
    scores = absolute(scores)
    print('Mean MAE: %.3f (%.3f)' % (mean(scores), std(scores)))

    list_row = ['Lasso', scores.mean()]
    interim.loc[len(interim)] = list_row

    ypred = model.predict(test_X)
    r2 = r2_score(test_y, ypred)
    print(f'R^2: {r2}')

    print('Ridge')

    from sklearn.linear_model import Ridge
    # define model
    model = Ridge(alpha=0.01, random_state=0)
    # define model evaluation method
    model = model.fit(train_X, train_y)
    cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
    # evaluate model
    scores = cross_val_score(model, train_X, train_y, scoring='neg_mean_absolute_error', cv=cv, n_jobs=-1)
    # force scores to be positive
    scores = absolute(scores)
    print('Mean MAE: %.3f (%.3f)' % (mean(scores), std(scores)))

    list_row = ['Ridge', scores.mean()]
    interim.loc[len(interim)] = list_row

    ypred = model.predict(test_X)
    r2 = r2_score(test_y, ypred)
    print(f'R^2: {r2}')

    print('ElasticNet')

    from sklearn.linear_model import ElasticNet
    model = ElasticNet(alpha=0.01, l1_ratio=0.5, random_state=0)
    model = model.fit(train_X, train_y)

    cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
    # evaluate model
    scores = cross_val_score(model, train_X, train_y, scoring='neg_mean_absolute_error', cv=cv, n_jobs=-1)
    # force scores to be positive
    scores = absolute(scores)
    print('Mean MAE: %.3f (%.3f)' % (mean(scores), std(scores)))

    list_row = ['ElasticNet', scores.mean()]
    interim.loc[len(interim)] = list_row

    ypred = model.predict(test_X)
    r2 = r2_score(test_y, ypred)
    print(f'R^2: {r2}')

    print('Decision Tree')

    from sklearn.tree import DecisionTreeRegressor
    regressor = DecisionTreeRegressor(random_state=0)
    # fit the regressor with X and Y data
    regressor.fit(train_X, train_y)
    ypred = regressor.predict(test_X)
    t1 = mean_absolute_error(test_y, ypred)
    print('Mean MAE: %.3f' %t1)

    list_row = ['Decision Tree', t1]
    interim.loc[len(interim)] = list_row

    r2 = r2_score(test_y, ypred)
    print(f'R^2: {r2}')

    print('Random Forest Regressor')
    from sklearn.ensemble import RandomForestRegressor

    rf = RandomForestRegressor(random_state=42, n_estimators=100)
    rf.fit(train_X, train_y)
    ypred = rf.predict(test_X)
    print("Random Forest R squared: {:.4f}".format(r2_score(test_y, ypred)))

    list_row = ['Random Forest', scores.mean()]
    interim.loc[len(interim)] = list_row

    add_columns_with_predictions(rf,pred_column, dataset[['Date']], X)

    print('Linear Regression')

    from sklearn.linear_model import LinearRegression
    linreg = LinearRegression()
    linreg.fit(train_X, train_y)
    ypred = linreg.predict(test_X)
    l1 = mean_absolute_error(test_y, ypred)
    print('Mean MAE: %.3f' %l1
          )
    list_row = ['Linear Regression', l1]
    interim.loc[len(interim)] = list_row

    return interim



results = work('adj_1_change')
results = results.drop('adj_1_change', axis=1)

for y in ['adj_1_change', 'adj_7_change', 'adj_30_change', 'adj_90_change']:
    interim = work(y)
    results = results.merge(interim, left_on='Model', right_on='Model')
    print('test')

#results = results.sort_values(by = 'MAE', ascending = False)
print(results)

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 8))
#Eyal change here
sns.barplot(x='adj_7_change', y='Model', data=results)
plt.show()