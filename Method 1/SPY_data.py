from Method1_data import start_date, end_date
import yfinance as yf
import pandas as pd
start_date = start_date
end_date = end_date
SPY_data = yf.download('SPY', start_date, end_date)
print(SPY_data)
