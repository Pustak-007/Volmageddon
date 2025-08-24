import wrds
import pandas as pd
import numpy as np
db = wrds.Connection()
print()
if __name__ == "__main__":
    pd.set_option('display.min_rows', 600)

ticker = 'SVXY'
#The two tickers that we are concerned with is SVXY or SPY
start_date = pd.Timestamp(2012,1,2)
end_date = pd.Timestamp(2023,2,27)
daily_index = pd.date_range(start = start_date, end = end_date)
def give_permno(target_ticker = ticker):
    permno_query = f"""select permno, ticker, comnam, namedt 
    from crsp.dsenames where ticker = '{target_ticker}' order by namedt desc"""
    helper_df = db.raw_sql(permno_query)
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
def give_price_data(ticker = ticker, start_date = pd.Timestamp(2012,1,2), end_date = pd.Timestamp(2023,2,27)):
    print(f'Fetching Historical Price Data for {ticker}')
    permno = give_permno(ticker)
    price_query = f"""SELECT date, permno, prc, vol, ret, cfacpr
    FROM crsp.dsf
    WHERE permno = {permno}
    AND date >= '{start_date}'
    AND date <= '{end_date}'"""
    daily_data = db.raw_sql(price_query, date_cols=['date'])
    daily_data['adj_price'] = abs(daily_data['prc'])/daily_data['cfacpr']
    return daily_data

def give_equity_curve(ticker = ticker):
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
    return equity_curve

print(give_permno('SVXY'))






