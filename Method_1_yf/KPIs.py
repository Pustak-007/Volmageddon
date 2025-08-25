# Okay so we have 5 periods and around 5 metrics:
import pandas as pd
import numpy as np
from Method1_data import start_date, end_date
from Method1_data import SVXY_data
from SPY_data import SPY_data
from StrategyVsBenchmark import SVXY_Unit_Equity_Curve, SPY_Unit_Equity_Curve
from USTY3MO import USTY3MO
from Drawdown import Calculate_Drawdown, Calculate_Max_Drawdown_Pct

def number_of_years(end_date, begin_date):
    b_date = pd.to_datetime(begin_date)
    e_date = pd.to_datetime(end_date)
    if e_date < b_date:
        raise ValueError ("Make sure you enter end_date first and begin_date second.")
    return ((e_date-b_date).days)/365.25

period_list = {'All' : (pd.Timestamp(2011,10,4), pd.Timestamp(2024,12,31)),
               'Golden Era' : (pd.Timestamp(2011,10,5), pd.Timestamp(2018,1,31)),
               'Volmageddon' : (pd.Timestamp(2018,2,1),pd.Timestamp(2018,2,28)),
               'Post-Volmageddon/Pre-COVID' : (pd.Timestamp(2018,3,1), pd.Timestamp(2020,1,31)),
               'COVID-19':(pd.Timestamp(2020,2,1), pd.Timestamp(2020,4,30)),
               'Post-COVID': (pd.Timestamp(2020,5,1), pd.Timestamp(2024,12,31))}

def give_KPIs(period, yahoo_data, unit_equity_curve):
    if period not in period_list:
        raise KeyError ("The given period is not in the period list")
    if period == "Volmageddon":
        raise KeyError("Annualized KPIs not applicable for Volmageddon - it was a short event")
    period_begin_date = period_list[period][0]
    period_end_date = period_list[period][1]
    def Calculate_CAGR(period):
        if yahoo_data.equals(SVXY_data):
            end_value = yahoo_data.loc[period_end_date, ('Close', 'SVXY')]
            begin_value = yahoo_data.loc[period_begin_date, ('Close', 'SVXY')]
        if yahoo_data.equals(SPY_data):
            end_value = yahoo_data.loc[period_end_date, ('Close', 'SPY')]
            begin_value = yahoo_data.loc[period_begin_date, ('Close', 'SPY')]
        Number_of_years = number_of_years(period_end_date, period_begin_date)
        CAGR = ((end_value/begin_value) ** (1/Number_of_years) - 1) * 100
        return CAGR
    def Calculate_Annualized_Volatility(period):
        daily_volatility = unit_equity_curve.loc[period_begin_date:period_end_date,'Daily PnL(%)'].std()
        trading_days_per_year = 252 #Standard Convention
        annualized_volatility = daily_volatility * np.sqrt(trading_days_per_year)
        return annualized_volatility
    def Calculate_Sharpe_Ratio(period):
        annual_vol = Calculate_Annualized_Volatility(period)
        expected_return = Calculate_CAGR(period)
        daily_excess_return = unit_equity_curve.loc[period_begin_date:period_end_date, 'Daily PnL(%)'] - (USTY3MO.loc[period_begin_date:period_end_date, 'Rates'] / 252)
        # we can de-annualize it using the compounding method as well, but the difference is negligible for daily returns.
        # so we will use the simple method here
        # Note that we need to subtract daily return of SVXY with daily return of USTY3MO
        #The rates in USTY3MO are different annualized yields for different days
        daily_excess_return.iloc[0] = np.nan
        #Daily Return of SVXY Long for 1st day - doesn't exist , so doens't make sense
        # -- to have excess return for that day
        annualized_excess_return = daily_excess_return.mean() * 252
        #general convention is to use 252 trading days in a year
        sharpe = annualized_excess_return/annual_vol
        return sharpe
    def Calculate_Max_Drawdown(period):
        my_data = yahoo_data.loc[period_begin_date:period_end_date]
        max_drawdown_pct = Calculate_Max_Drawdown_Pct(data = my_data)
        return max_drawdown_pct
    def Calculate_Skewness(period):
        skewness = unit_equity_curve.loc[period_begin_date:period_end_date, 'Daily PnL(%)'].skew()
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
def give_Volmageddon_KPIs(yahoo_data, unit_equity_curve, period = "Volmageddon"):
    if (yahoo_data != SVXY_data and yahoo_data!= SPY_data) or (unit_equity_curve!= SVXY_Unit_Equity_Curve or unit_equity_curve!= SPY_Unit_Equity_Curve):
        raise KeyError ('Data not accessible')
    period_begin_date = period_list[period][0]
    period_end_date = period_list[period][1]
    #calculate total cumulative return for the event 
    # -likely will be a large negative number close to 100
    def calculate_total_return():
        end_value = yahoo_data.loc[period_end_date, ('Close', 'SVXY')]
        begin_value = yahoo_data.loc[period_begin_date, ('Close', 'SVXY')]
        total_return_pct = (end_value - begin_value)/begin_value * 100
        return total_return_pct
    def calculate_daily_volatility():
        daily_volatility = unit_equity_curve.loc[period_begin_date:period_end_date,'Daily PnL(%)'].std()
        return daily_volatility
    def calculate_max_drawdown():
        my_data = yahoo_data.loc[period_begin_date:period_end_date]
        max_drawdown_pct = Calculate_Max_Drawdown_Pct(data = my_data)
        return max_drawdown_pct
    KPIs = pd.DataFrame()
    KPIs.index = ['Volmageddon']
    KPIs['Cumulative Return (%)'] = calculate_total_return()
    KPIs['Daily Volatility (%)'] = calculate_daily_volatility()
    KPIs['Maximmum Drawdown(%)'] = calculate_max_drawdown()
    return KPIs

if __name__ == "__main__":
    print(give_KPIs(period = 'Volmageddon', yahoo_data=SVXY_data, unit_equity_curve=SVXY_Unit_Equity_Curve))
    print(give_KPIs(period = 'Volmageddon', yahoo_data=SPY_data, unit_equity_curve=SPY_Unit_Equity_Curve))
 



        


