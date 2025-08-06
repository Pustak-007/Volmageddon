# Have your date range within 2011-10-04 to 2023-08-01
import time
import pandas as pd
import numpy as np
if __name__ == "__main__":
    pd.set_option('display.max_rows', None)
from one_month_test import PnL_of
big_dataframe = pd.DataFrame()
ticker = 'SPY' 
beginning_date = pd.Timestamp(2012,1,1)
ending_date = pd.Timestamp(2023,1,10)
def rolling_mechanism_test_df(ticker = ticker, beginning_date = beginning_date, ending_date = ending_date):
    from one_month_test import underlying_closing_price_at_exp_list, underlying_closing_price_at_open_list, call_strike_list, put_strike_list, total_premium_list, total_profit_list, total_payout_list
    from option_chain_func import list_of_relevant_valid_expiration_dates
    distinct_trading_dates_full = pd.to_datetime(pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/dinstinct_trading_dates.csv')['Dates'])
    #distinct_trading_dates = distinct_trading_dates_full[(distinct_trading_dates_full>=beginning_date) & (distinct_trading_dates_full<=ending_date)]
    rebalancing_days_full = pd.to_datetime(pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/first_trading_day_of_eachMonth.csv')['Dates'])
    rebalancing_days = rebalancing_days_full[(rebalancing_days_full>=beginning_date) & (rebalancing_days_full<=ending_date)]
    profit_list = [PnL_of(ticker, date) for date in rebalancing_days]
    converted_list = [float(x) for x in profit_list]

    #creation of the big dataframe - the dataframe to be displayed.
    big_dataframe.index = rebalancing_days
    big_dataframe.index.name = 'Open_Date'
    big_dataframe['Expiration_date'] = list_of_relevant_valid_expiration_dates
    big_dataframe['Underlying_at_Open'] = underlying_closing_price_at_open_list
    big_dataframe['Underlying_at_Expiraion'] = underlying_closing_price_at_exp_list
    big_dataframe['Call_Strikes'] = call_strike_list
    big_dataframe['Put_Strikes'] = put_strike_list
    big_dataframe['Total Premium Collected'] = total_premium_list
    big_dataframe['Total Payout'] = total_payout_list
    big_dataframe['Total PnL'] = total_profit_list
    if len(big_dataframe['Expiration_date']) != len(big_dataframe.index):
        raise ValueError("So, it seems we are not retrieving the updated list as you expected.")
    return big_dataframe
    #return converted_list
#df_to_store = rolling_mechanism_test_df()
#df_to_store.to_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/Final_PnL_DataFrame_Method_2.csv')
def rolling_mechanims_test_list(ticker = ticker, beginning_date = beginning_date, ending_date = ending_date):
    distinct_trading_dates_full = pd.to_datetime(pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/dinstinct_trading_dates.csv')['Dates'])
    #distinct_trading_dates = distinct_trading_dates_full[(distinct_trading_dates_full>=beginning_date) & (distinct_trading_dates_full<=ending_date)]
    rebalancing_days_full = pd.to_datetime(pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/first_trading_day_of_eachMonth.csv')['Dates'])
    rebalancing_days = rebalancing_days_full[(rebalancing_days_full>=beginning_date) & (rebalancing_days_full<=ending_date)]
    profit_list = [PnL_of(ticker, date) for date in rebalancing_days]
    converted_list = [float(x) for x in profit_list]
    return converted_list
start_time = time.time()
print(rolling_mechanism_test_df())
end_time = time.time()
#print(rolling_mechanims_test_list())
print(f"Execution time: {end_time - start_time}")





    
    



