import numpy as np
import pandas as pd
from StrategyVsBenchmark import SVXY_Unit_Equity_Curve
from USTY3MO import USTY3M0
if __name__ == "__main__":
    pd.set_option('display.min_rows', 200)
excess_return = SVXY_Unit_Equity_Curve['Daily PnL(%)'] - USTY3M0['Rates']
print(SVXY_Unit_Equity_Curve['Daily PnL(%)'])
print('-' * 100)
print(USTY3M0)
print('-'*100)
excess_return.iloc[0] = np.nan
#As we don't have the returns for the very first day - as there is no point of comparision
# -- so we set the excess return to be NaN for that day
print(excess_return)
