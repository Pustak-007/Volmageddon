#Okay so it seems that we may not require to retrieve our data using yfinance
from ib_insync import *
import pandas as pd
ib = IB()
ib.connect('127.0.0.1', port = 7497, clientId=1)
contract = Stock('SVXY', 'SMART', 'USD')
bars = ib.reqHistoricalData(contract, endDateTime='', durationStr='1 Y', 
                            barSizeSetting='1 day', whatToShow='ADJUSTED_LAST', 
                            useRTH=True)
df = util.df(bars)
print(df)
ib.disconnect()