import wrds 
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Method_2.option_chain_func import Rel_Options 
#see I have created most of the functions used in here in the module one_month_test.py
#but they appear as helper (inner) functions within a larger outer function - so I can't call them right here
# - So I am defining those functions here as standalone functions here.
db = wrds.Connection()
distinct_trading_dates = set(pd.to_datetime(pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/dinstinct_trading_dates.csv')['Dates']))
def permno_info(ticker)->pd.DataFrame:
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
SPY_permno = permno_of('SPY')
def give_daily_closing_price(ticker, date):
    if ticker != 'SPY':
        raise ValueError("The permno has been specified for SPY only, you can modify the give_daily_closing_price function in the margin_calculation_test module to make the fucntion more comprehensive")
    target_ticker = ticker
    target_date = date 
    price_query = f"""select date, permno, prc, abs(prc)/cfacpr as adjusted_price, cfacpr
        from crsp.dsf where permno = {SPY_permno} and date = '{target_date}'"""
    #this will likely return a dataframe with one row
    price_df = db.raw_sql(price_query)
    if price_df.empty:
        raise KeyError("Sorry, the date you have entered was not a trading day")
    return price_df['adjusted_price'].iloc[0]   

def Calculate_margin_of(ticker, date):
    if date not in distinct_trading_dates:
        raise KeyError("The date you have entered is not a valid trading day")
    relevant_options = Rel_Options(ticker, date)
    target_ticker = ticker 
    target_date = date 
    underlying_price = give_daily_closing_price(target_ticker, target_date)
    underlying_price_value = underlying_price * 100  # since options are typically on 100 shares
    put_premium_value = relevant_options.loc[1, 'best_bid'] * 100
    call_premium_value = relevant_options.loc[0, 'best_bid'] * 100
    def margin_for_put_option():
        # we know as a matter of fact that the put option is always going to be the second row in the dataframe returned by Rel_Options
        #Note that the data in the dataframe is not on the standard 100 shares basis, so we need to scale accordingly
        put_strike_value = relevant_options.loc[1, 'strike_price'] * 100
        ootm_amount = max(0, underlying_price_value - put_strike_value)
        m1 = (20/100 * underlying_price_value) - ootm_amount + put_premium_value
        m2 = (10/100 * put_strike_value) + put_premium_value
        m3 = 50 + put_premium_value
        return max(m1,m2,m3)
    def margin_for_call_option():
        call_strike_value = relevant_options.loc[0, 'strike_price'] * 100
        ootm_amount = max(0,call_strike_value - underlying_price_value)
        m1 = (20/100 * underlying_price_value) - ootm_amount + call_premium_value
        m2 = (10/100 * underlying_price_value) + call_premium_value
        m3 = 50 + call_premium_value
        return max(m1, m2, m3)
    margin_call = margin_for_call_option()
    margin_put = margin_for_put_option()
    if margin_call >= margin_put:
        return margin_call + put_premium_value
    else:
        return margin_put + call_premium_value
relevant_date = pd.Timestamp(2012,1,3)   
initial_margin = Calculate_margin_of('SPY', relevant_date)
if __name__ == "__main__":
    print(f"Initial margin for SPY on {relevant_date.date()}: {initial_margin}")

#Okay so initial margin for SPY on 2012-01-03 is 2313.4

#unlikely that we will be using this function again - but, anything can happen.