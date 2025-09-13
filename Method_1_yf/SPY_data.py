from Method1_data import start_date, end_date, daily_index
import yfinance as yf
import pandas as pd
start_date = start_date
end_date = end_date
SPY_data = yf.download('SPY', start_date, end_date + pd.Timedelta(days = 1))
SPY_data = SPY_data.reindex(index = daily_index)
'''
This was just for testing:

SPY_data2 = yf.download('SPY', pd.Timestamp(2011,12,20), pd.Timestamp(2023,2,17) + pd.Timedelta(days = 1))
daily_index2 = pd.date_range(pd.Timestamp(2011,12,20), pd.Timestamp(2023,2,17))
SPY_data2 = SPY_data2.reindex(index = daily_index2)
'''
if __name__ == "__main__":
  pd.set_option('display.min_rows', 200)
  #print(SPY_data)
  print(SPY_data)
