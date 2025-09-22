import sys, os
import pandas as pd
import numpy as np
if __name__ == "__main__":
    pd.set_option('display.min_rows', 300)
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # go up one folder
from Method_2.USTY3MO import USTY3MO
#print(USTY3MO)
short_strangle_unit_equity_data = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/Short Strangle Unit Equity Curve Data.csv', parse_dates=['date'], index_col=0)
print(short_strangle_unit_equity_data)
print(USTY3MO)
excess_return = short_strangle_unit_equity_data['Daily PnL(%)'] - USTY3MO['Rates']
print("The fun stuff: \n")
print(excess_return)