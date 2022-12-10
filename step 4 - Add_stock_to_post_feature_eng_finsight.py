#filter out dates from finsight
# Add +0 +1 +7 +30 +90
#Get filtered dates from stock file
#merge to Finsight source data
import pandas as pd


dict_cohort_files = {'AFRM': 'data/post feature eng/finsight_AFRM_post_feature_eng.csv',
                         'LC': 'data/post feature eng/finsight_LC_post_feature_eng.csv',
                        'OPRT': 'data/post feature eng/finsight_OPRT_post_feature_eng.csv',
                        'SOFI': 'data/post feature eng/finsight_SOFI_post_feature_eng.csv',
                        'UPST': 'data/post feature eng/finsight_UPST_post_feature_eng.csv'}

def manipulate(filename):
    df_finsight = pd.read_csv(filename)
    df_finsight['Date'] =  pd.to_datetime(df_finsight['Date'], format='%Y-%m-%d')

    df_stock = pd.read_csv('stocks/AFRM.csv')
    df_stock['Date'] =  pd.to_datetime(df_stock['Date'], format='%Y-%m-%d')

    date_list = df_finsight['Date'].values

    df_stock.set_index('Date', inplace = True)
    #https://stackoverflow.com/a/22898920/1384948
    df_stock_filtered = df_stock[df_stock.index.isin(date_list)]

    df_finsight.set_index('Date', inplace = True)

    final = df_finsight.merge(df_stock_filtered, left_index=True, right_on='Date')

    return final

for stock, file in dict_cohort_files.items():
    final = manipulate(file)
    final.to_csv(f'data/finsight/{stock}/file1_with_stock.csv')

print('end')