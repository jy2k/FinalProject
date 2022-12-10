import pandas as pd

dict_of_finsight_files = {'AFRM': 'Finsight source data/Finsight source data data - Affirm_edited_reformatted.csv',
                          'LC': 'Finsight source data/Finsight source data data - LC_edited_reformatted.csv',
                          'OPRT': 'Finsight source data/Finsight source data data - OPRT_edited_reformatted.csv',
                          'SOFI': 'Finsight source data/Finsight source data data - SoFi_edited_onlyESOT_reformatted.csv',
                          'UPST': 'Finsight source data/Finsight source data data - UPST_edited_reformatted.csv'}

KR_dict = {
    'AAA': 10,
    'AA': 9,
    'A': 8,
    'BBB': 7,
    'BB': 6,
    'B': 5,
    'CCC': 4,
    'CC': 3,
    'C': 2,
    'D': 1,
    'E': 0  }

MO_dict = {
    'Aaa': 10,
    'Aa': 9,
    'A': 8,
    'Baa': 7,
    'Ba': 6,
    'B': 5,
    'Caa': 4,
    'Ca': 3,
    'C': 2,
    'D': 1,
    'E': 0  }

columns_to_calc_change = ['CPN', 'KR', 'MO', 'PRICE', 'SPRD', 'SZE(M)', 'WAL', 'YLD']
# CPN: 3.46% , -, nan
# KR / MO: -, AAA, nan
# PRICE: -, 99.34, nan
# SPRD: -, 190, nan
# SZE(M): 150.00, nan
# WAL: -, 1.85, nan
# YLD: 3.46% , -, nan

def range_char(start, stop):
    return (chr(n) for n in range(ord(start), ord(stop) + 1))

i=0
for stock, file in dict_of_finsight_files.items():

    df = pd.read_csv(file)

    for col in columns_to_calc_change:
        for character in range_char("A", "E"):
            try:
                current_col = col+'-'+character
                new_col_name = str(current_col + '-change')

                if current_col in ['KR'+'-'+character, 'MO'+'-'+character]: #Need to handle - in the categorizing column before.
                    df[current_col] = df[current_col].replace(['-','nan'], 'E')
                    df[current_col] = df[current_col].astype('float')
                    if current_col == str('KR'+'-'+character):
                        df = df.replace({current_col: KR_dict})
                    if current_col == str('MO'+'-'+character):
                        df = df.replace({current_col: MO_dict})
                else:
                    df[current_col] = df[current_col].fillna(0)

                if current_col in ['CPN'+'-'+character, 'YLD'+'-'+character]:
                    df[current_col] = df[current_col].replace(['-'], '0.0')
                    df[current_col] = df[current_col].str.rstrip('%').astype('float') / 100.0

                if current_col in ['PRICE'+'-'+character, 'SPRD'+'-'+character, 'SZE(M)'+'-'+character, 'WAL'+'-'+character]:
                    df[current_col] = df[current_col].replace(['-'], '0.0')
                    df[current_col] = df[current_col].astype('float')

                df[new_col_name] = df[current_col].diff(periods=1)
            except:
                print(f'For file {file} - couldn\'t find column {character}')

    df.to_csv(f'data/post feature eng/finsight_{stock}_post_feature_eng.csv')
    i=i+1

print('end')
