import sys, os
import pandas as pd
import numpy as np
if __name__ == "__main__":
    pd.set_option('display.min_rows', 300)
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # go up one folder
distinct_trading_dates = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/dinstinct_trading_dates.csv', parse_dates=['Dates']).squeeze()
print(distinct_trading_dates)
my_dates = pd.date_range(pd.Timestamp(2011,10,4), pd.Timestamp(2011,11,14))
def helper_function(series):
    mask = series.isin(distinct_trading_dates)
    series = series[mask]
    return series
print(pd.Series(helper_function(my_dates)))