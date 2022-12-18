from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
import pandas as pd

dataset = pd.read_csv('Output data/cohort stock/AFRM/file_0_benchmark.csv')

dataset.dropna(axis=0, subset=['adj_1_change'], inplace=True)
y = dataset['adj_1_change'].astype('float')
X = dataset[['Life CDR','Open']].astype('float')

train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.25)

xgbr = XGBRegressor(objective='reg:squarederror')
xgbr.fit(train_X, train_y)
ypred = xgbr.predict(test_X)
mse = mean_squared_error(test_y, ypred)

print("RMSE: %.2f" % (mse ** (1 / 2.0)))

# Getting r_2_score
# https://scikit-learn.org/stable/modules/model_evaluation.html#r2-score-the-coefficient-of-determination
from sklearn.metrics import r2_score
r2 = r2_score(test_y, ypred)
print(f'R2: {r2}')