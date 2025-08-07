"""import pandas as pd
s = pd.to_datetime(pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/dinstinct_trading_dates.csv')['Dates'])
print(pd.Timestamp(2014,3,3) in s.values)
"""
import wrds 
import pandas as pd
db = wrds.Connection()
permno_query = """select permno, ticker, comnam, namedt from crsp.dsenames
where ticker = 'SPY' order by namedt desc"""
permno_df = db.raw_sql(permno_query)
#print(permno_df)
SPY_permno = permno_df['permno'].iloc[0]
print(SPY_permno)
daily_closing_price_query = f"""select date, permno, prc, abs(prc)/cfacpr as adjusted_price, cfacpr\
    from crsp.dsf where permno = {SPY_permno} and date = '{pd.Timestamp(2014,3,3)}'"""
my_df = db.raw_sql(daily_closing_price_query)
my_price = my_df['adjusted_price'].iloc[0]
print(my_df)




