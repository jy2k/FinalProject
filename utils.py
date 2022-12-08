import pandas as pd

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


def filter_date(data, day_of_the_month):
    start = data['Date'].iloc[0]
    end = data['Date'].iloc[-1]

    data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')
    data.set_index('Date', inplace=True)

    dates = pd.date_range(data.first_valid_index().normalize(), end=data.last_valid_index(), freq='D')
    dates = dates[dates.day == day_of_the_month]

    df_filtered = data.reindex(dates, method='nearest')

    return df_filtered