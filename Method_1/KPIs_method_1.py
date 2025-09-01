#The code and most of the functions will be similar to the KPIs.py file in Method_1

#The regimes we are analyzing have to be the same as the ones as Longing SVXY Method
# - This is done for the sake of consistency.

import pandas as pd
import numpy as np
from Drawdown_method_1 import Calculate_Max_Drawdown_Pct, Calculate_Drawdown
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
               'COVID-19':(pd.Timestamp(2020,2,1), pd.Timestamp(2020,4,30)),
               'Post-COVID': (pd.Timestamp(2020,5,1), pd.Timestamp(2023,2,17))}
#yeah - also the realization that most of the code is going to be the same as the other one.
#Note that yahoo_data represents different things in this instance and in 

#Not needed
#ss_strategy_unit_equity_curve = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/Short Strangle Unit Equity Curve Data.csv', parse_dates=['date'])
#benchmark_unit_equity_curve = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/SPY Unit Equity Curve Data.csv', parse_dates=['date'])
#
spy_unit_equity_curve = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/SPY Unit Equity Curve Data.csv', parse_dates=['date'], index_col=0)
svxy_unit_equity_curve = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/SVXY Unit Equity Curve Data.csv', parse_dates=['date'], index_col=0)
#lets just have both as zero right now, but I will have to extract the relevant data from wrds
def give_KPIs(period, unit_equity_curve):
    if period not in period_list:
        raise KeyError ("The given period is not in the period list")
    if period == "Volmageddon":
        raise KeyError("Annualized KPIs not applicable for Volmageddon - it was a short event")
    period_begin_date = period_list[period][0]
    period_end_date = period_list[period][1]
    range_mask = (unit_equity_curve['date'] >= period_begin_date) & (unit_equity_curve['date'] <= period_end_date)
    def Calculate_CAGR(period):
        end_value = unit_equity_curve.loc[unit_equity_curve['date'] == period_end_date, 'equity'].iloc[0]
        begin_value = unit_equity_curve.loc[unit_equity_curve['date'] == period_begin_date, 'equity'].iloc[0]
        print(end_value)
        print(begin_value)
        Number_of_years = number_of_years(period_end_date, period_begin_date)
        print(Number_of_years)
        CAGR = ((end_value/begin_value) ** (1/Number_of_years) - 1) * 100
        return CAGR
    def Calculate_Annualized_Volatility(period):
        daily_volatility = unit_equity_curve.loc[range_mask,'Daily PnL(%)'].std()
        trading_days_per_year = 252 #Standard Convention
        annualized_volatility = daily_volatility * np.sqrt(trading_days_per_year)
        return annualized_volatility
    #Note that sharpe_ratio is generally given in annualized terms - so sharpe_ratio 
    # is the same as annualized_sharpe
    def Calculate_Sharpe_Ratio(period):

        risk_free_rate = USTY3MO['Rates']
        #This risk free rate is annualized

        #de-annualized risk free rate
        daily_risk_free_rate = (1 + risk_free_rate)**(1/252) - 1
        daily_returns = unit_equity_curve['Daily PnL(%)'].copy()
        daily_excess_returns = daily_returns - daily_risk_free_rate
        average_daily_excess_return = daily_excess_returns.mean()
        daily_sharpe = average_daily_excess_return/daily_returns.std()
        annualized_sharpe = daily_sharpe * np.sqrt(252)
        return annualized_sharpe
    def Calculate_Max_Drawdown(period):
        rel_equity_data = unit_equity_curve.loc[range_mask]
        max_drawdown_pct = Calculate_Max_Drawdown_Pct(rel_equity_data)
        return max_drawdown_pct
    def Calculate_Skewness(period):
        skewness = unit_equity_curve.loc[range_mask, 'Daily PnL(%)'].skew()
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
    period_begin_date = period_list[period][0]
    period_end_date = period_list[period][1]
    range_mask = (unit_equity_curve['date'] >= period_begin_date) & (unit_equity_curve['date'] <= period_end_date)
    def calculate_total_return():
        end_value = unit_equity_curve.loc[unit_equity_curve['date'] == period_begin_date, 'equity']
        begin_value = unit_equity_curve.loc[unit_equity_curve['date'] == period_end_date, 'equity']
        total_return_pct = (end_value - begin_value)/begin_value * 100
        return total_return_pct
    def calculate_daily_volatility():
        daily_volatility = unit_equity_curve.loc[range_mask,'Daily PnL(%)'].std()
        return daily_volatility
    def calculate_max_drawdown():
        rel_data = unit_equity_curve[range_mask]
        max_drawdown_pct = Calculate_Max_Drawdown_Pct(rel_data)
        return max_drawdown_pct
    KPIs = pd.DataFrame()
    KPIs.index = ['Volmageddon']
    KPIs['Cumulative Return (%)'] = calculate_total_return()
    KPIs['Daily Volatility (%)'] = calculate_daily_volatility()
    KPIs['Maximmum Drawdown(%)'] = calculate_max_drawdown()
    return KPIs
if __name__ == "__main__":
    print(give_KPIs(period = 'All', unit_equity_curve=spy_unit_equity_curve))
    #Test over whether the CAGR that I got is correct or not.
    start_series = spy_unit_equity_curve.iloc[1]
    start_date = start_series['date']
    start_value = start_series['equity']
    end_series = spy_unit_equity_curve.iloc[-1]
    end_date = end_series['date']
    end_value = end_series['equity']
    Number_of_years = number_of_years(end_date, start_date)
    #print((start_series['equity'], end_series['equity'], start_series['date'], end_series['date']))
    print(f"Number of years = {Number_of_years}")
    CAGR = ((end_value/start_value) ** (1/Number_of_years) - 1) * 100
    print(CAGR)
    print('-'*100)
    print(start_series)
    print('-'*100)
    print(end_series)
    print('-'*100)
    print(spy_unit_equity_curve[spy_unit_equity_curve['date'] == pd.Timestamp(2012,1,3)])
    print(spy_unit_equity_curve[spy_unit_equity_curve['date'] == pd.Timestamp(2023,2,17)])
    print('-'*100)
    print(spy_unit_equity_curve)
