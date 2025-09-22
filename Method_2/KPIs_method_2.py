#The code and most of the functions will be similar to the KPIs.py file in Method_1

#The regimes we are analyzing have to be the same as the ones as Longing SVXY Method
# - This is done for the sake of consistency.

import pandas as pd
import numpy as np
from Drawdown_method_2 import Calculate_Max_Drawdown_Pct, Calculate_Drawdown
from USTY3MO import USTY3MO

def number_of_years(end_date, begin_date):
    b_date = pd.to_datetime(begin_date)
    e_date = pd.to_datetime(end_date)
    if e_date < b_date:
        raise ValueError ("Make sure you enter end_date first and begin_date second.")
    return ((e_date-b_date).days)/365.25

period_list = {'All' : (pd.Timestamp(2012,1,3), pd.Timestamp(2023,2,17)),
               'Golden Era' : (pd.Timestamp(2012,1,3), pd.Timestamp(2018,1,31)),
               'Volmageddon' : (pd.Timestamp(2018,2,1),pd.Timestamp(2018,2,28)),
               'Post-Volmageddon/Pre-COVID' : (pd.Timestamp(2018,3,1), pd.Timestamp(2020,1,31)),
               'COVID-19':(pd.Timestamp(2020,2,1), pd.Timestamp(2021,2,1)),
               'Post-COVID': (pd.Timestamp(2021,2,2), pd.Timestamp(2023,2,17))}
#yeah - also the realization that most of the code is going to be the same as the other one.
#Note that yahoo_data represents different things in this instance and in 
ss_strategy_unit_equity_curve = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/Short Strangle Unit Equity Curve Data.csv', parse_dates=['date'],index_col = 0)
benchmark_unit_equity_curve = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/SPY Unit Equity Curve Data.csv', parse_dates=['date'], index_col = 0)
distinct_valid_trading_days_series = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/dinstinct_trading_dates.csv', parse_dates=['Dates']).squeeze()
distinct_valid_trading_days = set(distinct_valid_trading_days_series.values)
#lets just have both as zero right now, but I will have to extract the relevant data from wrds
def give_KPIs(period, unit_equity_curve):
    if period not in period_list:
        raise KeyError ("The given period is not in the period list")
    if period == "Volmageddon":
        raise KeyError("Annualized KPIs not applicable for Volmageddon - it was a short event")
    period_begin_date = period_list[period][0]
    period_end_date = period_list[period][1]
    if (period_begin_date not in distinct_valid_trading_days or period_end_date not in distinct_valid_trading_days):
        #raise ValueError ("it seems one of the major demarcation days falls to be a holiday - need to change the implement the sliding logic accordingly")
        print("Oh! It seems that one of the demarcation days for this period is a holiday or not a valid trading day - we are implementing forward roll of the day")
        old_period_begin_date = period_begin_date
        old_period_end_date = period_end_date
        while period_begin_date not in distinct_valid_trading_days:
            period_begin_date = period_begin_date + pd.Timedelta(days = 1)
            #we don't want the period_begin_date to go before the regime initial date
        while period_end_date not in distinct_valid_trading_days:
            period_end_date = period_end_date - pd.Timedelta(days = 1)
            #we don't want the period_end_date to go after the regime end date
        print(f"Old Period Begin Date: {old_period_begin_date}")
        print(f"New Period Begin Date: {period_begin_date}")
        print(f"Old Period End Date: {old_period_end_date}")
        print(f"New Period End Date: {period_end_date}")
    else:
        pass
        #print(f"begin date = {period_begin_date.date()}")
        #print(f"end date = {period_end_date.date()}")    
    range_mask = (unit_equity_curve['date'] >= period_begin_date) & (unit_equity_curve['date'] <= period_end_date)
    def Calculate_CAGR(period):
        end_value = unit_equity_curve.loc[unit_equity_curve['date'] == period_end_date, 'equity'].iloc[0]
        begin_value = unit_equity_curve.loc[unit_equity_curve['date'] == period_begin_date, 'equity'].iloc[0]
        if period_begin_date == pd.Timestamp(2012,1,3):
           begin_value = 1
        if end_value<=0 or begin_value <= 0:
            raise ValueError("Equity Values can't be negative or zero.")
        print(f"end value = {end_value}")
        print(f"begin value = {begin_value}")
        Number_of_years = number_of_years(period_end_date, period_begin_date)
        print(f"Number of years = {Number_of_years}")
        CAGR = ((end_value/begin_value) ** (1/Number_of_years) - 1) * 100
        return CAGR
    def Calculate_Annualized_Volatility(period):
        daily_returns_ser = unit_equity_curve.loc[range_mask, 'Daily PnL(%)']
        daily_returns_ser = daily_returns_ser[daily_returns_ser!=0]
        daily_volatility = daily_returns_ser.std()
        trading_days_per_year = 252 #Standard Convention
        annualized_volatility = daily_volatility * np.sqrt(trading_days_per_year)
        return annualized_volatility
    #Note that sharpe_ratio is generally given in annualized terms - so sharpe_ratio 
    # is the same as annualized_sharpe
    def Calculate_Sharpe_Ratio(period):

        #risk free relevant rate for the period
        risk_free_rate = USTY3MO.loc[(USTY3MO['date'] >= period_begin_date) & (USTY3MO['date'] <= period_end_date), 'Rates']
        #This risk free rate is annualized

        #de-annualized risk free rate
        daily_risk_free_rate = ((1 + risk_free_rate/100)**(1/252) - 1) * 100
        daily_returns = unit_equity_curve['Daily PnL(%)'].loc[range_mask].copy()
        daily_excess_returns = daily_returns - daily_risk_free_rate
        average_daily_excess_return = daily_excess_returns.mean()
        daily_sharpe = average_daily_excess_return/daily_excess_returns.std()
        annualized_sharpe = daily_sharpe * np.sqrt(252)
        return annualized_sharpe
    def Calculate_Max_Drawdown(period):
        rel_equity_data = unit_equity_curve.loc[range_mask]
        max_drawdown_pct = Calculate_Max_Drawdown_Pct(rel_equity_data)
        return max_drawdown_pct
    def Calculate_Skewness(period):
        relevent_ser = unit_equity_curve.loc[range_mask, 'Daily PnL(%)']
        relevent_ser = relevent_ser[relevent_ser!=0]
        skewness = relevent_ser.skew()
        return skewness
    KPIs = pd.DataFrame(index = [period])
    KPIs['CAGR(%)'] = Calculate_CAGR(period)
    KPIs['Annualized Volatility(%)'] = Calculate_Annualized_Volatility(period)
    KPIs['Sharpe Ratio'] = Calculate_Sharpe_Ratio(period)
    KPIs['Max Drawdown(%)'] = Calculate_Max_Drawdown(period)
    KPIs['Skewness'] = Calculate_Skewness(period)
    return KPIs

#Separate function for Volmageddon KPIs
# - since it is a short event and we don't need annualized KPIs
def give_Volmageddon_KPIs(unit_equity_curve, period = "Volmageddon"):
    if period != 'Volmageddon':
        raise KeyError("This function is explicitly for Volmageddon period - please use the give_KPIs function for this regime")
    period_begin_date = period_list[period][0]
    period_end_date = period_list[period][1]
    range_mask = (unit_equity_curve['date'] >= period_begin_date) & (unit_equity_curve['date'] <= period_end_date)
    def calculate_total_return():
        end_value = unit_equity_curve.loc[unit_equity_curve['date'] == period_end_date, 'equity'].iloc[0]
        begin_value = unit_equity_curve.loc[unit_equity_curve['date'] == period_begin_date, 'equity'].iloc[0]
        print(f"end value = {end_value}")
        print(f"begin value = {begin_value}")
        total_return_pct = (end_value - begin_value)/begin_value * 100
        return total_return_pct
    def calculate_daily_volatility():
        daily_returns_ser = unit_equity_curve.loc[range_mask,'Daily PnL(%)']
        daily_returns_ser = daily_returns_ser[daily_returns_ser!=0]
        daily_volatility = daily_returns_ser.std()
        return daily_volatility
    def calculate_max_drawdown():
        rel_data = unit_equity_curve[range_mask]
        drawdown_data  = Calculate_Drawdown(rel_data)
        max_drawdown_pct = Calculate_Max_Drawdown_Pct(rel_data)
        return max_drawdown_pct
    KPIs = pd.DataFrame()
    KPIs.index = ['Volmageddon']
    KPIs['Cumulative Return (%)'] = calculate_total_return()
    KPIs['Daily Volatility (%)'] = calculate_daily_volatility()
    KPIs['Max Drawdown(%)'] = calculate_max_drawdown()
    return KPIs
if __name__ == "__main__":
    print("Short Strangle Strategy KPIs: ")
    #print(give_KPIs(period = 'COVID-19', unit_equity_curve=ss_strategy_unit_equity_curve))
    print(give_Volmageddon_KPIs(unit_equity_curve=ss_strategy_unit_equity_curve))
    print("SPY KPIs: ")
    print(give_Volmageddon_KPIs(unit_equity_curve=benchmark_unit_equity_curve))