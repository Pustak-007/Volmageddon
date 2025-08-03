import wrds
import pandas as pd
db = wrds.Connection()

#I have given the function - for SPY it works, and it will mostly work for other companies
# as well, but always better to have one glance at the entire dataframe (row not limited to 1)
# to understand it, better to take a look at the output of secid_info function first just for assurance
# rather than blindly trusting the secid_of function's result.
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
    print(f"\nRetrieving the full option_chain data for {ticker} on {target_date}, it may take some seconds ...\n")
    option_chain_query = f"""
    select secid, date, exdate, cp_flag, strike_price/1000 as strike_price, best_bid, best_offer, volume, impl_volatility, delta, gamma, vega, theta
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
    print (f"\n Retrieving the 30-45 day expiration range option_chain data for {ticker} on {target_date}, it may take some seconds ...\n")
    option_chain_query = f"""
    select secid, date, exdate, cp_flag, strike_price/1000 as strike_price, best_bid, best_offer, volume, impl_volatility, delta, gamma, vega, theta
    from optionm.opprcd{relevant_year}
    where secid = {underlying_secid} and date = '{target_date}'
    and exdate between (date '{target_date}' + interval '30 days') and (date '{target_date}' + interval '45 days')"""
    option_chain_data = db.raw_sql(option_chain_query)
    option_chain_data_refined = option_chain_data[option_chain_data['impl_volatility']!='<NA>']
    return option_chain_data_refined

#This function only to be used for first trading day of the month, I may 
# --impose this constraint later on.
def Rel_Options(ticker, date) -> pd.DataFrame:
    rel_chain = Rel_Option_Chain(ticker, date)
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
    option_chain = Rel_Options('SPY', pd.Timestamp(2020,10,12))
    print (option_chain)
    if option_chain.empty:
        print("Empty Dataframe indicates that the given day was a weekend.")
    
