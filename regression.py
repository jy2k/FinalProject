
import pandas as pd
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv('data/cohort stock/AFRM/file_0.csv', index_col=0)

import statsmodels.api as sm
import statsmodels.formula.api as smf

results = smf.ols('Close ~ Low', data=df).fit()
print(results.summary())
print('end')