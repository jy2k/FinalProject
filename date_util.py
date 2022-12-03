import pandas as pd

def filter_date(data, day_of_the_month):
    start = data['Date'].iloc[0]
    end = data['Date'].iloc[-1]

    data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')
    data.set_index('Date', inplace=True)

    dates = pd.date_range(data.first_valid_index().normalize(), end=data.last_valid_index(), freq='D')
    dates = dates[dates.day == day_of_the_month]

    df_filtered = data.reindex(dates, method='nearest')

    return df_filtered