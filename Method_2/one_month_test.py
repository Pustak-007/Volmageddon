import wrds 
import random
import pandas as pd 
from option_chain_func import Rel_Options, test_date
date_range = pd.date_range(pd.Timestamp(2012,1,1), pd.Timestamp(2023,8,1))
test_date =  pd.Timestamp(2014,3,3)#random.choice(date_range)
db = wrds.Connection()
closing_price_at_open_list = list()
closing_price_at_exp_list = list()
call_strike_list = list()
put_strike_list = list()
total_profit_list = list()
def PnL_of(ticker = 'SPY', date = test_date):
    df = Rel_Options(ticker, date)
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
        price_query = f"""select date, permno, prc, abs(prc)/cfacpr as adjusted_price, cfacpr
        from crsp.dsf where permno = {permno_of(target_ticker)} and date = '{target_date}'"""
        price_df = db.raw_sql(price_query)
        if price_df.empty:
            raise KeyError("Sorry, the date you have entered was not a trading day")
        return price_df['adjusted_price'].iloc[0]
    call_exp_date = pd.Timestamp(df.loc[0, 'last_trade_date'])
    put_exp_date = pd.Timestamp(df.loc[1, 'last_trade_date'])

    open_date_closing_price = daily_closing_price('SPY', date)
    closing_price_at_open_list.append(open_date_closing_price) 
    closing_price_for_call_payout = daily_closing_price(ticker, call_exp_date)
    closing_price_for_put_payout = daily_closing_price(ticker, put_exp_date)
    if (closing_price_for_call_payout!=closing_price_for_put_payout):
        raise ValueError("Same exp for put and call => same closing price of SPY for both")
    closing_price_at_exp_list.append(closing_price_for_call_payout)
    exp_call_strike = df.loc[0,'strike_price']
    call_strike_list.append(exp_call_strike)
    exp_put_strike = df.loc[1,'strike_price']
    put_strike_list.append(exp_put_strike)
  
    call_payout = max(0, round((closing_price_for_call_payout - exp_call_strike),2))
    put_payout = max(0, round((exp_put_strike - closing_price_for_put_payout),2))

    total_profit = round((total_premium_collected - call_payout - put_payout),2) 
    total_profit_list.append(total_profit)   
    #
    """
    
    print("\n The closing prices for call_payout and put_payout are: \n")
    print([float(SPY_closing_price_for_call_payout), float(SPY_closing_price_for_put_payout)])

    print(f'\n{df}')
    print(f'\n Total premium collected: {total_premium_collected}')
    print(f'\n Call Payout : {call_payout}')
    print(f'\n Put Payout : {put_payout}')
    print(f'\n Profit : {round(total_profit,2)}')
    """
    #
    return total_profit
if __name__ == "__main__":
    print(PnL_of())
