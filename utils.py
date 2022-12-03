def concat_csvs(list_csvs):
    df_full = pandas.DataFrame()

    for csv in list_csvs:
        current = pandas.read_csv(csv, index_col=0)
        df_full = df_full.append(current)

    return df_full

def bucketize_date(val, full_month_format):
    interim = datetime.strptime(val, full_month_format)
    month = str(interim.month)
    year = str(interim.year)
    new_format = str(month + '/' + year)
    return new_format