#May be we won't be needing this module right here.

import wrds
import pandas as pd
import numpy as np
from functools import partial
db = wrds.Connection()
print()
if __name__ == "__main__":
    pd.set_option('display.min_rows', 600)

ticker = 'SVXY'
#The two tickers that we are concerned with is SVXY or SPY
start_date = pd.Timestamp(2012,1,2)
end_date = pd.Timestamp(2023,2,17)
daily_index = pd.date_range(start = start_date, end = end_date)
def give_permno(target_ticker = ticker):
    permno_query = f"""select permno, ticker, comnam, namedt 
    from crsp.dsenames where ticker = '{target_ticker}' order by namedt desc"""
    helper_df = db.raw_sql(permno_query, date_cols=['date'])
    if helper_df.empty:
        raise ValueError('Could not find a valid permno for the given ticker')
    permno = helper_df['permno'].iloc[0]
    return permno

"""
Result:
SPY Permno in CRSP = 84398
SVXY Permno in CRSP = 13029
"""
print()
def give_price_data(ticker = ticker, start_date = start_date, end_date = end_date):
    print(f'Fetching Historical Price Data for {ticker}...\n')
    permno = give_permno(ticker)
    price_query = f"""SELECT date, permno, prc, vol, ret, cfacpr
    FROM crsp.dsf
    WHERE permno = {permno}
    AND date >= '{start_date}'
    AND date <= '{end_date}'"""
    daily_data = db.raw_sql(price_query, date_cols=['date'])
    if daily_data.empty:
        raise ValueError("No permno corresponding to this ticker")
    daily_data['adj_price'] = abs(daily_data['prc'])/daily_data['cfacpr']
    return daily_data

def give_equity_curve(ticker = ticker):     
    permno = give_permno(ticker)     
    data = give_price_data(ticker)     
    equity_curve = pd.DataFrame()     
    equity_curve['date'] = data['date']     
    equity_curve['equity'] = data['adj_price']     
    equity_curve['Daily PnL(%)'] = ((equity_curve['equity'].pct_change()) * 100).fillna(0)     
    equity_curve['Cumulative PnL(%)'] = ((1 + equity_curve['Daily PnL(%)']/100).cumprod() - 1).fillna(0)     
    equity_curve = equity_curve.set_index('date')     
    equity_curve = equity_curve.reindex(daily_index)     
    equity_curve.index.name = 'date'     
    equity_curve = equity_curve.reset_index()     
    equity_curve['equity'] = equity_curve['equity'].ffill()     
    equity_curve['Daily PnL(%)'] = equity_curve['Daily PnL(%)'].fillna(0)     
    equity_curve['Cumulative PnL(%)'] = equity_curve['Cumulative PnL(%)'].fillna(0)
    if pd.isna(equity_curve.iloc[0]['equity']):        
       helper_date = equity_curve.iloc[0]['date']
       temp = equity_curve.iloc[0]['equity']
      
       while pd.isna(temp):            
           helper_date = helper_date - pd.Timedelta(days=1)            
           helper_query = f"""select date, prc, cfacpr, abs(prc)/cfacpr as adj_price            
           from crsp.dsf             
           where date = '{helper_date}' and permno = {permno}"""            
           helper_df = db.raw_sql(helper_query)            
           if not helper_df.empty:                
               temp = helper_df['adj_price'].iloc[0]             
      
       equity_curve.loc[0,'equity'] = temp      
       #easier to re-calculate the entire series rather than write the code about changing one element specifically
       # - and this manual practice can lead to another edge case, this change of everything is easier. 
       equity_curve['Daily PnL(%)'] = (equity_curve['equity'].pct_change() * 100).fillna(0)
       equity_curve['Cumulative PnL(%)'] = ((1 + equity_curve['Daily PnL(%)']/100).cumprod() - 1) * 100
    return equity_curve
def give_unit_equity_curve(ticker):
    equity_curve = give_equity_curve(ticker)
    initial_capital = 1
    unit_equity_curve = pd.DataFrame()
    unit_equity_curve['date'] = equity_curve['date'].copy()
    unit_equity_curve['Daily PnL(%)'] = equity_curve['Daily PnL(%)'].copy()
    unit_equity_curve['Growth Factor'] = 1 + unit_equity_curve['Daily PnL(%)']/100
    unit_equity_curve['equity'] = initial_capital * unit_equity_curve['Growth Factor'].cumprod()
    unit_equity_curve['Cumulative PnL(%)'] = ((1 + unit_equity_curve['Daily PnL(%)']/100).cumprod() - 1) * 100
    return unit_equity_curve
"""

give_SPY_equity_curve = partial(give_equity_curve, 'SPY')
give_SVXY_equity_curve = partial(give_equity_curve, 'SVXY')

give_SPY_unit_equity_curve = partial(give_unit_equity_curve, 'SPY')
give_SVXY_unit_equity_curve = partial(give_unit_equity_curve, 'SVXY')

SPY_unit_equity_curve = give_SPY_unit_equity_curve()
SVXY_unit_equity_curve = give_SVXY_unit_equity_curve()

SPY_equity_curve = give_SPY_equity_curve()
SVXY_equity_curve = give_SVXY_equity_curve()

#functions to store the data 
def store_SPY_unit_equity_curve():
    SPY_unit_equity_curve.to_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/SPY Unit Equity Curve Data.csv')
def store_SVXY_unit_equity_curve():
    SVXY_unit_equity_curve.to_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/SVXY Unit Equity Curve Data.csv')
def store_SPY_equity_curve():
    SPY_equity_curve.to_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/SPY Equity Curve Data.csv')
def store_SVXY_equity_curve():
    SVXY_equity_curve.to_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/SVXY Equity Curve Data.csv')

"""
if __name__ == "__main__":
    print(give_equity_curve('SVXY'))
            





