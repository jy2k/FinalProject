from sklearn import linear_model, metrics, model_selection
from sklearn.linear_model import LinearRegression
import pandas as pd

df = pd.read_csv('data/cohort stock/AFRM/AFRM-cohort-stock.csv', index_col=0)

X = df['Gross_Coupon'].values.reshape(-1, 1)
y = df['Close'].values.reshape(-1, 1)

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size = 0.2)

regressor = LinearRegression()
regressor.fit(X_train, y_train)
print(regressor.intercept_)
print(regressor.coef_)

score = regressor.predict([[9.5]])
print(score) # 94.80663482

print('end')