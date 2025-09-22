
#Think of last_trade_date as the actual expiration date and exdate as the legal expiration date
import wrds
import pandas as pd
db = wrds.Connection()
if __name__ == "__main__":
    pd.set_option('display.min_rows', 400)
valid_trading_dates = set(pd.to_datetime(pd.read_csv("/Users/pustak/Desktop/Volmageddon/Local_Data/dinstinct_trading_dates.csv")['Dates']))
test_date = pd.Timestamp(2014,3,3)
list_of_relevant_valid_expiration_dates = list()
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
def Rel_Option_Chain(ticker: str , date: pd.Timestamp) -> pd.DataFrame:
    target_date = date
    relevant_year = date.year
    required_options = pd.DataFrame()
    print(f"\n Finding the most feasible option expiration date to short for {target_date.date()} ... ")
    secid_query = f"""
        select secid, cusip, effect_date, issuer, issue
        from optionm.secnmd
        where ticker = '{ticker}'
        order by effect_date desc limit 1
    """
    info = db.raw_sql(secid_query)
    underlying_secid = info['secid'].iloc[0]

    event_date = date + pd.Timedelta(days=45)
    best_exdate_query = f"""
        select exdate from optionm.opprcd{relevant_year} 
        where secid = {underlying_secid} and date = '{date}' 
        order by abs(exdate - date '{event_date}') limit 2
    """
    best_exdate_info = db.raw_sql(best_exdate_query)
    if not best_exdate_info.empty:
        best_exdate = pd.Timestamp(best_exdate_info['exdate'].iloc[0])
        display_best_date = best_exdate
        while display_best_date not in valid_trading_dates:
            display_best_date = display_best_date - pd.Timedelta(days=1)
        list_of_relevant_valid_expiration_dates.append(display_best_date)
        print(f"\n The best valid expiration date seems to be {display_best_date.date()}")
        print(f"\n Retrieving the option chain data for {ticker} on {target_date.date()}({weekday_dict[target_date.weekday()]}) with expiration day on {display_best_date.date()}({weekday_dict[display_best_date.weekday()]}) , it may take some seconds .. ")
        required_options_query = f"""
        select secid, date, exdate, date '{display_best_date}' as last_trade_date,
        cp_flag, strike_price/1000 as strike_price, best_bid, best_offer, volume, impl_volatility, delta, gamma, vega, theta
        from optionm.opprcd{relevant_year}
        where secid = {underlying_secid} and date = '{target_date}' and exdate = '{best_exdate}'
        """
        required_options = db.raw_sql(required_options_query)
        required_options = required_options[required_options['impl_volatility'].notna()]
        print("-" * 100)
    else:
        print(f"\n Opps! Given Date : {target_date.date()}({weekday_dict[target_date.weekday()]}) seems not to be a valid trading day, here is the information for the next valid day:")
    return required_options


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
    if rel_options_df['last_trade_date'].iloc[0] != rel_options_df['last_trade_date'].iloc[1]:
        raise ValueError('Same expiration date constraint got violated!')
    return rel_options_df

#for testing
if __name__ == "__main__":
    option_chain = Rel_Options('SPY', test_date)
    print (option_chain)
    if option_chain.empty:
        print("Empty Dataframe indicates that the given day was a weekend/non-trading day.")
    
