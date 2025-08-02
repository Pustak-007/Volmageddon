import wrds
import time
import pandas as pd
db = wrds.Connection()
#print(db.describe_table(library='optionm', table = 'secnmd')['name'])
target_ticker = 'SPY'
target_date = pd.Timestamp(2020,10,12)
relevant_year = target_date.year
secid_query = f"""
select secid, cusip, effect_date, issuer, issue 
from optionm.secnmd 
where ticker = '{target_ticker}'
order by effect_date desc limit 1"""
underlying_info = db.raw_sql(secid_query)
underlying_secid = underlying_info['secid'].iloc[0]
print(f"The secid of {target_ticker} in WRDS Database is: {underlying_secid}")
#Query for retrieving option chain for the given date
print("\n Retrieving Option Chain, this may take some seconds ... \n")
start_time = time.time()
option_chain_query = f"""
select secid, date, exdate, cp_flag, strike_price/1000 as strike_price, best_bid, best_offer, volume, impl_volatility, delta, gamma, vega, theta
from optionm.opprcd{relevant_year}
where secid = {underlying_secid} and date = '{target_date}'"""
option_chain_data = db.raw_sql(option_chain_query)
option_chain_data_refined = option_chain_data[option_chain_data['impl_volatility']!='<NA>']
end_time = time.time()
print(option_chain_data_refined)
print("\nThe discrepency between row numbering and number of rows due to removal of options with incalculate implied volatility")
print(f'\nOptions with incalculable implied volatility = {len(option_chain_data) - len(option_chain_data_refined)}')
print(f'\nTime taken for option chain retrieval = {end_time - start_time}')


