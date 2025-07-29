from Method1_data import start_date, end_date, daily_index
import yfinance as yf
import pandas as pd
start_date = start_date
end_date = end_date
SPY_data = yf.download('SPY', start_date, end_date + pd.Timedelta(days = 1))
SPY_data = SPY_data.reindex(index = daily_index)
if __name__ == "__main__":
  pd.set_option('display.min_rows', 200)
  print(SPY_data)
