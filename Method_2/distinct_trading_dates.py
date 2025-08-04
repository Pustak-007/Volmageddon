import wrds 
import pandas as pd
beginning_date = pd.Timestamp(2010,11,4)
end_date = pd.Timestamp(2023,7,29)
import wrds 
db = wrds.Connection()

def give_distinct_trading_dates(start = beginning_date, end = end_date):
    distinct_date_query = f"""select distinct date from crsp.dsf
    where date between '{start}' and '{end}' order by date desc"""
    helper_df = db.raw_sql(distinct_date_query)
    return helper_df
if __name__ == "__main__":
    pd.set_option('display.min_rows', 600)
    #print(give_distinct_trading_dates())
    trading_day_series = give_distinct_trading_dates()
    trading_day_series.to_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/dinstinct_trading_dates.csv', index = False)
    