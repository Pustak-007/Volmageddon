#This is a test for the use of iBKR api and ib_insync library

from ib_insync import *
ib = IB()
ib.connect('127.0.0.1', 7497, clientId = 1)
contract = Stock('AAPL', 'SMART', 'USD')
bars = ib.reqHistoricalData(contract, durationStr='1 Y', endDateTime='', whatToShow='ADJUSTED_LAST',
                              barSizeSetting='1 day', useRTH=True)
df = util.df(bars)
df.set_index(df['date'], inplace = True)
df.drop('date', axis = 1, inplace = True)
print(df)

