import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

dataset = pd.read_csv('Output data/cohort stock/AFRM/file_0_benchmark.csv')

def add_columns(df):
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.str.replace('+', '')
    df['Gross_Coupon_Minus_Annualized_Net_Loss_Rate'] = df['Gross_Coupon'].subtract(df['Annualized_Net_Loss_Rate'])
    df['d1_dist_from_bench'] = df['adj_1_change'] - df['avg_adj_1_change']
    df['d7_dist_from_bench'] = df['adj_7_change'] - df['avg_adj_7_change']
    df['d30_dist_from_bench'] = df['adj_30_change'] - df['avg_adj_30_change']
    df['d90_dist_from_bench'] = df['adj_90_change'] - df['avg_adj_90_change']
    return df
dataset = add_columns(dataset)
dataset.dropna(axis=0, subset=['adj_1_change'], inplace=True)
y = dataset['adj_1_change'].astype('float')
X = dataset[['Annualized_Net_Loss_Rate', 'Life_CDR']].astype('float')

train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.1)

xgbr = XGBRegressor(objective='reg:squarederror')
xgbr.fit(train_X, train_y)
ypred = xgbr.predict(test_X)
# https://scikit-learn.org/stable/modules/model_evaluation.html#r2-score-the-coefficient-of-determination
from sklearn.metrics import r2_score
r2 = r2_score(test_y, ypred)
print(f'R2: {r2}')

from numpy import mean
from numpy import std
from numpy import absolute
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold
from sklearn.linear_model import Lasso

model = Lasso(alpha=0.01)
# define model evaluation method
cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
# evaluate model
scores = cross_val_score(model, train_X, train_y, scoring='neg_mean_absolute_error', cv=cv, n_jobs=-1)
# force scores to be positive
scores = absolute(scores)
print('Mean MAE: %.3f (%.3f)' % (mean(scores), std(scores)))

from sklearn.linear_model import Ridge
# define model
model = Ridge(alpha=0.01)
# define model evaluation method
cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
# evaluate model
scores = cross_val_score(model, train_X, train_y, scoring='neg_mean_absolute_error', cv=cv, n_jobs=-1)
# force scores to be positive
scores = absolute(scores)
print('Mean MAE: %.3f (%.3f)' % (mean(scores), std(scores)))


from sklearn.linear_model import ElasticNet
model = ElasticNet(alpha=0.01, l1_ratio=0.5)

cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
# evaluate model
scores = cross_val_score(model, train_X, train_y, scoring='neg_mean_absolute_error', cv=cv, n_jobs=-1)
# force scores to be positive
scores = absolute(scores)
print('Mean MAE: %.3f (%.3f)' % (mean(scores), std(scores)))


from sklearn.tree import DecisionTreeRegressor
regressor = DecisionTreeRegressor(random_state=0)
# fit the regressor with X and Y data
regressor.fit(train_X, train_y)
ypred = regressor.predict(test_X)
r2 = r2_score(test_y, ypred)
print(f'R2: {r2}')