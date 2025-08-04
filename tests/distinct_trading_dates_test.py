import wrds 
import pandas as pd
if __name__ == "__main__":
    pd.set_option('display.min_rows', 600)
db = wrds.Connection()
def give_distinct_trading_dates(start = pd.Timestamp(2011,10,4) , end = pd.Timestamp(2023, 7, 29)):
    distinct_date_query = f"""select distinct date from crsp.dsf
    where date between '{start}' and '{end}' order by date desc"""
    helper_df = db.raw_sql(distinct_date_query)
    return helper_df
date_series = give_distinct_trading_dates()
date_series.to_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/dinstinct_trading_dates.csv', index = False)
#print(str(pd.Timestamp(2012,1,3).date()) in date_series.values)
# Okay, so it does work as I expect it to work then - that is pretty interesting.