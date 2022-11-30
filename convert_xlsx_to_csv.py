import pandas as pd

filename = 'public/Affirm/20-1/AFRM20Z1_20221011.xlsx'
df = pd.read_excel(filename)
df.to_csv('public/Affirm/20-1/AFRM20Z1_20221011.csv')
print('end')
