import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import yfinance as yf 
from matplotlib.ticker import FixedFormatter, FixedLocator, NullLocator
data = yf.download('SVXY', start = pd.Timestamp(2011,10,1), end = pd.Timestamp.now())
print(data)

#Visualization
fig, ax = plt.subplots(figsize = (16,8), dpi = 100)
ax.plot(data.index,data['Close'])

ax.set_xlabel('Date', fontsize = 14)
ax.set_ylabel('Value', fontsize = 14)
ax.set_yscale('log')
y_ticks = [10,20,30,40,50,70,100,150,200]
ax.yaxis.set_major_locator(FixedLocator(y_ticks))
ax.yaxis.set_major_formatter(FixedFormatter(y_ticks))
ax.yaxis.set_minor_locator(NullLocator())
ax.xaxis.set_major_locator(mdates.YearLocator(1))
ax.xaxis.set_minor_locator(mdates.MonthLocator(interval = 2))
plt.title('SVXY Index Log Figure', fontsize = 14)
plt.tight_layout()
plt.show(),