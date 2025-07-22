import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import yfinance as yf 
data = yf.download('SVXY', start = pd.Timestamp(2011,10,1), end = pd.Timestamp.now())
print(data)
fig, ax = plt.subplots()
x = data.index
y = data['Close']
ax.plot(x,y)
ax.set_xlabel('Date')
ax.set_ylabel('Value')
ax.set_yscale('log')
ax.xaxis.set_major_locator(mdates.YearLocator(1))
ax.xaxis.set_minor_locator(mdates.MonthLocator(interval = 2))
plt.tight_layout()
plt.show()