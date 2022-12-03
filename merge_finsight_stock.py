import pandas as pd

dict_stocks_finsight = {'AFRM': 'Finsight/Finsight data - Affirm_edited_reformatted.csv',
        'LC': 'Finsight/Finsight data - LC_edited_reformatted.csv',
        'OPRT': 'Finsight/Finsight data - OPRT_edited_reformatted.csv',
        'SOFI': 'Finsight/Finsight data - SoFi_edited_onlyESOT_reformatted.csv',
        'UPST': 'Finsight/Finsight data - UPST_edited_reformatted.csv'
}

for stock, finsight_file in dict_stocks_finsight.items():

    lc_finsight_df = pd.read_csv(finsight_file, index_col=0)
    lc_stock_df = pd.read_csv(f'stocks/{stock}.csv')

    lc_finsight_stocks_df = lc_finsight_df.merge(lc_stock_df, left_index=True, right_on = 'Date')
    lc_finsight_stocks_df = lc_finsight_stocks_df.set_index('Date')

    lc_finsight_stocks_df.to_csv(f'data/finsight/{stock}/file1.csv')








