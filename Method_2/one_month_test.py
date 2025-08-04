import wrds 
import pandas as pd 
from option_chain_func import Rel_Options, test_date
db = wrds.Connection()
df = Rel_Options('SPY', test_date)
if df.empty:
    raise ValueError('The dataframe containing relevant options to trade should not be empty')
total_premium_collected = sum(df['best_bid'])
def permno_info(ticker) -> pd.DataFrame:
    target_ticker = ticker
    permno_query = f"""select permno, ticker, comnam, namedt 
    from crsp.dsenames where ticker = '{target_ticker}' order by namedt desc"""
    permno_df = db.raw_sql(permno_query)
    return permno_df

def permno_of(ticker):
    target_ticker = ticker
    permno_query = f"""select permno, ticker, comnam, namedt 
    from crsp.dsenames where ticker = '{target_ticker}' order by namedt desc"""
    permno_df = db.raw_sql(permno_query)
    return permno_df['permno'].iloc[0]

def daily_closing_price(ticker, date):
    target_ticker = ticker
    target_date = date.date()
    price_query = f"""select date, permno, prc, prc/cfacpr as adjusted_price, cfacpr
    from crsp.dsf where permno = {permno_of(target_ticker)} and date = '{target_date}'"""
    price_df = db.raw_sql(price_query)
    if price_df.empty:
        raise KeyError("Sorry, the date you have entered was not a trading day")
    return price_df['prc'].iloc[0]
call_exp_date = pd.Timestamp(df.loc[0, 'last_trade_date'])
put_exp_date = pd.Timestamp(df.loc[1, 'last_trade_date'])

SPY_closing_price_for_call_payout = daily_closing_price('SPY', call_exp_date)
SPY_closing_price_for_put_payout = daily_closing_price('SPY', put_exp_date)

SPY_exp_call_strike = df.loc[0,'strike_price']
SPY_exp_put_strike = df.loc[1,'strike_price']

call_payout = max(0, SPY_closing_price_for_call_payout - SPY_exp_call_strike)
put_payout = max(0, SPY_exp_put_strike - SPY_closing_price_for_put_payout)

total_profit = total_premium_collected - call_payout - put_payout

print("\n The closing prices for call_payout and put_payout are: \n")
print([float(SPY_closing_price_for_call_payout), float(SPY_closing_price_for_put_payout)])

print(f'\n{df}')
print(f'\n Total premium collected: {total_premium_collected}')
print(f'\n Call Payout : {call_payout}')
print(f'\n Put Payout : {put_payout}')
print(f'\n Profit : {total_profit}')

