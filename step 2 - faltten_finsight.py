# This script takes 1 finsight file at a time and flattens it
# This file wasn't fully automated with a for loop because it only ever needed to be run once on 5 files.
import pandas as pd

filename = 'Finsight source data/Finsight data - SoFi_edited_onlyESOT.csv'
initial = pd.read_csv(filename)
pd.to_datetime(initial['Date'])
initial['Date'] = pd.to_datetime(initial['Date'])

out = (
    initial
    .pivot(index='Date', 
           columns='CLASS', 
           values=['CCY','SZE(M)','WAL','MO','SP','FI','DR','KR','C/E','LTV','TYPE','BNCH','GDNC','SPRD','CPN','YLD','PRICE'])
    .sort_index(axis=1, level=1))

out.columns = out.columns.map(lambda x: f"{x[0]}-{x[1]}")

out = out.sort_index()

new_col = initial.groupby(['Date'])['SZE(M)'].sum()
out.insert(loc=0, column='Sum SZE(M)', value=new_col)
print(out.index)

out.sort_index()
out.to_csv(filename+'_reformatted.csv')
print('done')