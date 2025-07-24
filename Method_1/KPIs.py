# Okay so we have 5 periods and around 5 metrics:
import pandas as pd
import numpy as np
from Method1_data import start_date, end_date
from Method1_data import SVXY_data
from StrategyVsBenchmark import SVXY_Unit_Equity_Curve, SPY_Unit_Equity_Curve
from USTY3MO import USTY3MO
from Drawdown import Calculate_Drawdown, Calculate_Max_Drawdown_Pct
def number_of_years(end_date, begin_date):
    b_date = pd.to_datetime(begin_date)
    e_date = pd.to_datetime(end_date)
    if e_date < b_date:
        raise ValueError ("Make sure you enter end_date first and begin_date second.")
    return ((e_date-b_date).days)/365.25
period_list = {'All' : (pd.Timestamp(2011,10,5), pd.Timestamp(2024,12,30)),
               'Golden Era' : (pd.Timestamp(2011,10,5), pd.Timestamp(2018,1,31)),
               'Volmageddon' : (pd.Timestamp(2018,2,1),pd.Timestamp(2018,2,28)),
               'Post-Volmageddon/Pre-COVID' : (pd.Timestamp(2018,3,1), pd.Timestamp(2020,1,31)),
               'COVID-19':(pd.Timestamp(2020,2,1), pd.Timestamp(2020,4,30)),
               'Post-COVID': (pd.Timestamp(2020,5,1), pd.Timestamp(2024,12,30))}
def give_KPIs(period, yahoo_data, unit_equity_curve):
    if period not in period_list:
        raise KeyError ("The given period is not in the period list")
    def Calculate_CAGR(period):
        end_value = yahoo_data.loc[period_list[period][1], 'Close']
        begin_value = yahoo_data.loc[period_list[period][0], 'Close']
        Number_of_years = number_of_years(period_list[period][1], period_list[period][0])
        CAGR = (end_value/begin_value) ** (1/number_of_years) - 1
        return CAGR
    def Calculate_Annualized_Volatility(period):
        daily_volatility = unit_equity_curve['Daily PnL(%)'].std()
        trading_days_per_year = 252 #Standard Convention
        annualized_volatility = daily_volatility * np.sqrt(trading_days_per_year)
        return annualized_volatility
    def Calculate_Sharpe_Ratio(period):
        annual_vol = Calculate_Annualized_Volatility(period)
        expected_return = Calculate_CAGR(period)
        daily_excess_return = unit_equity_curve['Daily PnL(%)'] - (USTY3MO.loc[period_list[period][0]:period_list[period][1], 'Rates'] / 252)
        # Note that we need to subtract daily return of SVXY with daily return of USTY3MO
        #The rates in USTY3MO are different annualized yields for different days
        daily_excess_return.iloc[0] = np.nan
        #Daily Return of SVXY Long for 1st day - doesn't exist , so doens't make sense
        # -- to have excess return for that day
        annualized_excess_return = daily_excess_return.mean() * 252
        sharpe = annualized_excess_return/annual_vol
        return sharpe
    def Calculate_Max_Drawdown(period):
        my_data = yahoo_data.loc[period_list[period][0]:period_list[period][1]]
        max_drawdown_pct = Calculate_Max_Drawdown_Pct(data = my_data)
        return max_drawdown_pct
    def Calculate_Skewness(period):
        skewness = unit_equity_curve['Daily PnL(%)'].skew()
        return skewness
    





        


