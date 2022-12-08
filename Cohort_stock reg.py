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

plt.rc("figure", figsize=(16, 8))
plt.rc("font", size=14)

df = pd.read_csv('/Users/eyalben-eliyahu/PycharmProjects/FinalProject/data/cohort stock/AFRM/file_0.csv', index_col=0)

# ['1mo_CPR', 'Gross_Coupon', 'Accum_Net_Loss%',
#        'Annualized_Net_Loss_Rate', 'Delinq_30+', 'Number_of_Assets',
#        'Life_CDR', 'Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume',
#        'Monthly_Change']

df.columns = df.columns.str.replace(' ', '_')
df.columns = df.columns.str.replace('+', '')
df['Monthly_Change'] = df['Adj_Close'].pct_change()
df = df.dropna()
df['Gross_Coupon_Minus_Annualized_Net_Loss_Rate'] = df['Gross_Coupon'].subtract(df['Annualized_Net_Loss_Rate'])


results = smf.ols('Monthly_Change ~ Life_CDR + Delinq_30 + Annualized_Net_Loss_Rate', data=df).fit()
print(results.summary())

plt.plot(df['Gross_Coupon_Minus_Annualized_Net_Loss_Rate'])
plt.show()