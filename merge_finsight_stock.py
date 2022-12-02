from sklearn import linear_model, metrics, model_selection
from sklearn.linear_model import LinearRegression
import pandas as pd

lc_finsight_df = pd.read_csv('/Users/eyalben-eliyahu/PycharmProjects/FinalProject/Finsight/Finsight data - LC_edited_reformatted.csv', index_col=0)
lc_stock_df = pd.read_csv('/Users/eyalben-eliyahu/PycharmProjects/FinalProject/stocks/LC.csv')

lc_finsight_stocks_df = lc_finsight_df.merge(lc_stock_df, left_index=True, right_on = 'Date')
lc_finsight_stocks_df = lc_finsight_stocks_df.set_index('Date')

lc_finsight_stocks_df.to_csv("lc_finsight_stocks_df")








