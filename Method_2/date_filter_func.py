import pandas as pd
date_index = pd.to_datetime(pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/dinstinct_trading_dates.csv').squeeze())
def filter_tradingDay_closestTo_monthStart(date_index = date_index):
    df = pd.DataFrame({'dates': date_index})
    closest_dates = df.groupby([df['dates'].dt.year, df['dates'].dt.month])['dates'].min()
    closest_dates_series = pd.Series([d.strftime('%Y-%m-%d') for d in closest_dates])
    closest_dates_series.name = 'Dates'
    return closest_dates_series

def store_first_tradingDay_of_eachMonth():
    relevant_series = filter_tradingDay_closestTo_monthStart()
    relevant_series.to_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/first_trading_day_of_eachMonth.csv', index = False)

if __name__ == "__main__":
    store_first_tradingDay_of_eachMonth()
