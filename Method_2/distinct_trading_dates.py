import wrds 
import pandas as pd
beginning_date = pd.Timestamp(2011,10,4)
end_date = pd.Timestamp(2023,8,1)
import wrds 
db = wrds.Connection()

def give_distinct_trading_dates(start = beginning_date, end = end_date):
    distinct_date_query = f"""select distinct date from crsp.dsf
    where date between '{start}' and '{end}' order by date desc"""
    helper_df = db.raw_sql(distinct_date_query)
    helper_df.rename(columns = {'date':'Dates'}, inplace=True)
    return helper_df
if __name__ == "__main__":
    pd.set_option('display.min_rows', 600)
    #print(give_distinct_trading_dates())
    trading_day_series = give_distinct_trading_dates()
    trading_day_series.to_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/dinstinct_trading_dates.csv', index = False)
def give_number_of_trading_days(start = beginning_date, end = end_date):
    trading_days = give_distinct_trading_dates(start, end)
    return len(trading_days)    
if __name__ == "__main__":
    start_date = pd.Timestamp(2012,1,3)
    end_date = pd.Timestamp(2012,2,17)
    test_variable = give_number_of_trading_days(start_date, end_date)
    print(test_variable)
    print('-'*100)
    print(-0.27/test_variable)
    