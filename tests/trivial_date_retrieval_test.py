import pandas as pd
valid_trading_days = set(pd.to_datetime(pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/dinstinct_trading_dates.csv')['Dates']))
print(pd.Timestamp(2014,4,18) in valid_trading_days)
