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
def Option_Chain(ticker, date) -> pd.DataFrame:
    print(f"\nRetrieving the option_chain data for {ticker} on {date.date()}, it may take some seconds ...\n")
    underlying_secid = secid_of(ticker)
    target_date = date
    relevant_year = target_date.year
    option_chain_query = f"""
    select secid, date, exdate, cp_flag, strike_price/1000 as strike_price, best_bid, best_offer, volume, impl_volatility, delta, gamma, vega, theta
    from optionm.opprcd{relevant_year}
    where secid = {underlying_secid} and date = '{target_date}'"""
    option_chain_data = db.raw_sql(option_chain_query)
    option_chain_data_refined = option_chain_data[option_chain_data['impl_volatility']!='<NA>']
    return option_chain_data_refined

#for testing
if __name__ == "__main__":
    option_chain = Option_Chain('SPY', pd.Timestamp(2020,10,12))
    print (option_chain)
    if option_chain.empty:
        print("Empty Dataframe indicates that the given day was a weekend.")

    
    
