from ib_insync import *
import matplotlib.pyplot as plt 
import pandas as pd
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)
contract = Option('AAPL', '20250829', 210, 'C', exchange= 'SMART')
end_date = pd.Timestamp(2025,7,25).strftime("%Y%m%d %H:%M:%S")
bars = ib.reqHistoricalData(
    contract,
    endDateTime=end_date,
    durationStr='1 M',
    barSizeSetting='1 hour',
    whatToShow='TRADES',
    useRTH=True
)
df = util.df(bars)
df.index = df['date']
df.drop('date', axis = 1, inplace = True)
print(df)
x = df.index
y = df['close']
plt.plot(x,y, color = 'blue', linewidth = 1.3)
plt.show()