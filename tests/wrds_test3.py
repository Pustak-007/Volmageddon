import wrds 
import pandas as pd
db = wrds.Connection()
target_ticker = 'SPY'
#well first lets just create a function that will give me the closing price
# -- on a point of time.
permno_query = f"""select permno, ticker, comnam, namedt 
from crsp.dsenames where ticker = '{target_ticker}' order by namedt desc"""
helper_df = db.raw_sql(permno_query)
permno = helper_df['permno'].iloc[0]
date = pd.Timestamp(2020,10,12)
price_query = f"""select date, permno, prc, prc/cfacpr as adjusted_price, cfacpr, vol from crsp.dsf where permno = {permno} and date = '{date}'"""
price_df = db.raw_sql(price_query)['adjusted_price'].iloc[0]
print(price_df)
#print(db.describe_table(library='crsp', table = 'dsf'))
#print(helper_df)
#print(permno)