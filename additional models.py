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
print('Mean MAE: %.3f (%.3f)' % (scores.mean(), scores.std()))

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
print('Mean MAE: %.3f' % t1)

list_row = ['Decision Tree', t1]
interim.loc[len(interim)] = list_row

r2 = r2_score(test_y, ypred)
print(f'R^2: {r2}')

print('Linear Regression')

from sklearn.linear_model import LinearRegression

linreg = LinearRegression()
linreg.fit(train_X, train_y)
ypred = linreg.predict(test_X)
l1 = mean_absolute_error(test_y, ypred)
print('Mean MAE: %.3f' % l1)

list_row = ['Linear Regression', l1]
interim.loc[len(interim)] = list_row
