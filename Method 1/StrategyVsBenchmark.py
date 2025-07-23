from Method1_data import SVXY_data
from SPY_data import SPY_data
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
from matplotlib.ticker import FixedFormatter, FixedLocator, NullLocator
import matplotlib.dates as mdates
from functools import partial
initial_capital = 1 #Standard practice to make returns comparative and readable

#Creation of SVXY Unit Equity Curve Data
def Create_UnitDollar_Equity_Curve(data):
    equity_curve = pd.DataFrame()
    equity_curve.index = data.index
    equity_curve['PnL (%)'] = (data['Close'].pct_change() * 100).fillna(0)
    equity_curve['Growth Factor'] = 1 + (equity_curve['PnL (%)'])/100
    equity_curve['Equity'] = initial_capital * equity_curve['Growth Factor'].cumprod()
    return equity_curve

Create_UnitDollar_SVXY_Equity_Curve = partial(Create_UnitDollar_Equity_Curve, data = SVXY_data)
Create_UnitDollar_SPY_Equity_Curve = partial(Create_UnitDollar_Equity_Curve, data = SPY_data)
equity_curve1 = Create_UnitDollar_SVXY_Equity_Curve()
equity_curve2 = Create_UnitDollar_SPY_Equity_Curve()

def Plot_UnitDollar_SVXYvsSPY_Equity_Curve():
    fig, ax = plt.subplots(figsize = (16,8), dpi = 100)
    x = equity_curve1.index
    y = equity_curve1['Equity']
    x2 = equity_curve2.index
    y2 = equity_curve2['Equity']
    ax.plot(x,y, label = "SVXY (Strategy)", color = 'blue')
    ax.plot(x2,y2, label = "SPY (Benchmark)", color = 'purple')
    ax.grid(True, alpha = 0.3)
    ax.set_xlabel("Date", fontsize = 14)
    ax.set_ylabel("Equity Value", fontsize = 14)
    ax.set_yscale('log')
    #manual y_ticks
    y_ticks = [1,2,5,10,15,20,25]
    ax.yaxis.set_major_locator(FixedLocator(y_ticks))
    ax.yaxis.set_major_formatter(FixedFormatter(y_ticks))
    ax.yaxis.set_minor_locator(NullLocator())
    
    # X-axis formatting
    ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    ax.legend()
    plt.title("SVXY Unit Equity Return vs SPY Unit Equity Return (Log Scale)", fontsize = 16, fontweight = 'bold')
    plt.show()

if __name__ == "__main__":
    Plot_UnitDollar_SVXYvsSPY_Equity_Curve()








