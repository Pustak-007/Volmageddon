#⚠️⚠️This module is suitable for unit testing but not suitable for
# -- incorporating into the backtest - primarily due to the number of text messages involved.


import wrds
import pandas as pd
db = wrds.Connection()
if __name__ == "__main__":
    pd.set_option('display.min_rows', 400)

test_date = pd.Timestamp(2012,1,5)
#I have given the function - for SPY it works, and it will mostly work for other companies
# as well, but always better to have one glance at the entire dataframe (row not limited to 1)
# to understand it, better to take a look at the output of secid_info function first just for assurance
# rather than blindly trusting the secid_of function's result.
weekday_dict = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}
def secid_info(ticker):
    secid_query = f"""
    select secid, cusip, effect_date, issuer, issue 
    from optionm.secnmd 
    where ticker = '{ticker}'
    order by effect_date desc"""
    secid_info_df = db.raw_sql(secid_query)
    return secid_info_df

def secid_of(ticker):
    secid_query = f"""
    select secid, cusip, effect_date, issuer, issue 
    from optionm.secnmd 
    where ticker = '{ticker}'
    order by effect_date desc limit 1"""
    underlying_info = db.raw_sql(secid_query)
    underlying_secid = underlying_info['secid'].iloc[0]
    return underlying_secid

#Function to retrieve all the available options available to trade on a specific day
def Full_Option_Chain(ticker, date) -> pd.DataFrame:
    
    underlying_secid = secid_of(ticker)
    target_date = date.date()
    relevant_year = target_date.year
    print(f"\n Retrieving the full option_chain data for {ticker} on {target_date} ({weekday_dict[target_date.weekday()]}), it may take some seconds ...")
    option_chain_query = f"""
    select 
    secid, date, exdate, 
    case when extract(dow from exdate) = 6 then exdate  - interval '1 day' else exdate
    end as last_trade_date,
    cp_flag, strike_price/1000 as strike_price, best_bid, best_offer, volume, impl_volatility, delta, gamma, vega, theta
    from optionm.opprcd{relevant_year}
    where secid = {underlying_secid} and date = '{target_date}'"""
    option_chain_data = db.raw_sql(option_chain_query)
    option_chain_data_refined = option_chain_data[option_chain_data['impl_volatility']!='<NA>']
    return option_chain_data_refined

#Function for the options whose expiration is such that there is no gamma risk and
# --time horizon for profit realization is also feasible
def Rel_Option_Chain(ticker, date) -> pd.DataFrame:
    underlying_secid = secid_of(ticker)
    target_date = date.date()
    relevant_year = target_date.year
    print (f"\n Retrieving the 30-45 day expiration range option_chain data for {ticker} on {target_date} ({weekday_dict[target_date.weekday()]}), it may take some seconds ...")
    option_chain_query = f"""
    select secid, date, exdate, 
    case when extract(dow from exdate) = 6 then exdate - interval '1 day' else exdate
    end as last_trade_date,
    cp_flag, strike_price/1000 as strike_price, best_bid, best_offer, volume, impl_volatility, delta, gamma, vega, theta
    from optionm.opprcd{relevant_year}
    where secid = {underlying_secid} and date = '{target_date}'
    and exdate between (date '{target_date}' + interval '30 days') and (date '{target_date}' + interval '45 days')"""
    option_chain_data = db.raw_sql(option_chain_query)
    option_chain_data_refined = option_chain_data[option_chain_data['impl_volatility']!='<NA>']
    if option_chain_data_refined.empty:
        if not Full_Option_Chain(ticker,date).empty:
            print(f"\n It seems that on {target_date} ({weekday_dict[target_date.weekday()]}), within the tight window of 30-45 day expiration range we can't find any tradable options, let's expand the window to 30-60 expiration range")
            print (f"\n Retrieving the 30-60 day expiration range option_chain data for {ticker} on {target_date} ({weekday_dict[target_date.weekday()]}), it may take some seconds ...")
            option_chain_query = f"""
            select secid, date, exdate,
            case when extract(dow from exdate) = 6 then exdate - interval '1 day' else exdate
            end as last_trade_date,
            cp_flag, strike_price/1000 as strike_price, best_bid, best_offer, volume, impl_volatility, delta, gamma, vega, theta
            from optionm.opprcd{relevant_year}
            where secid = {underlying_secid} and date = '{target_date}'
            and exdate between (date '{target_date}' + interval '30 days') and (date '{target_date}' + interval '60 days')"""
            option_chain_data = db.raw_sql(option_chain_query)
            option_chain_data_refined = option_chain_data[option_chain_data['impl_volatility']!='<NA>']
            if option_chain_data_refined.empty:
                raise ValueError(' It failed, the logic of expanding window manually is not comprehensive enough to work in every case!')
        else:
            # This block will only be executed if both the full_option_chain and refined_option_chain are empty
            # -- which indicates that there was no trading activity on this day.
            print("\n Oops! It seems that the given day was not a valid trading day, retrieving data for the next day:")
            print('-' * 100)
    return option_chain_data_refined

#This function only to be used for first trading day of the month, I may 
# --impose this constraint later on.
def Rel_Options(ticker, date) -> pd.DataFrame:
    rel_chain = Rel_Option_Chain(ticker, date)
    current_date = date
    while rel_chain.empty:
        current_date = current_date + pd.Timedelta(days = 1)
        rel_chain = Rel_Option_Chain(ticker, current_date)
    pos_delta_target = 0.25
    neg_delta_target = -0.25
    #index of row with delta value closest to 0.25
    closest_pos_delta_index = (rel_chain['delta'] - pos_delta_target).abs().idxmin()
    #index of row with delta value closest to -0.25
    closest_min_delta_index = (rel_chain['delta'] - neg_delta_target).abs().idxmin()
    rel_options_df = pd.concat([rel_chain.loc[[closest_pos_delta_index]], rel_chain.loc[[closest_min_delta_index]]], ignore_index=True)
    return rel_options_df

#for testing
if __name__ == "__main__":
    option_chain = Rel_Options('SPY', test_date)
    print (option_chain)
    if option_chain.empty:
        print("Empty Dataframe indicates that the given day was a weekend/non-trading day.")
    
