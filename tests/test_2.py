import yfinance as yf 
import pandas as pd
start_date = pd.Timestamp(2020,10,1)
end_date = pd.Timestamp(2024,10,1)
data = yf.download(tickers='AAPL', start = start_date, end = end_date)
print(data.head(10))
print('-' * 100)
a = data.loc[pd.Timestamp(2020,10,20), ('Close', 'AAPL')]
print(a)
#But if she is not replying, then that largely means that the extended access to bloomberg
# is generally not accessible.