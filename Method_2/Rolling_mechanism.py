# Have your date range within 2011-10-04 to 2023-08-01
import time
import pandas as pd
import numpy as np
from one_month_test import PnL_of
ticker = 'SPY' 
start_time = time.time()
beginning_date = pd.Timestamp(2012,1,1)
ending_date = pd.Timestamp(2023,1,1)
def rolling_mechanism_test(ticker = ticker, beginning_date = beginning_date, ending_date = ending_date):
    distinct_trading_dates_full = pd.to_datetime(pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/dinstinct_trading_dates.csv')['Dates'])
    distinct_trading_dates = distinct_trading_dates_full[(distinct_trading_dates_full>=beginning_date) & (distinct_trading_dates_full<=ending_date)]
    rebalancing_days_full = pd.to_datetime(pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/first_trading_day_of_eachMonth.csv')['Dates'])
    rebalancing_days = rebalancing_days_full[(rebalancing_days_full>=beginning_date) & (rebalancing_days_full<=ending_date)]
    profit_list = [PnL_of(ticker, date) for date in rebalancing_days]
    converted_list = [float(x) for x in profit_list]
    return converted_list
#the list returned will contain floats in np.
print(rolling_mechanism_test())
end_time = time.time()
print(f"Execution time: {end_time - start_time}")




    
    



