from Method1_data import SVXY_data
from SPY_data import SPY_data
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
from matplotlib.ticker import FixedFormatter, FixedLocator, NullLocator
import matplotlib.dates as mdates
from functools import partial
if __name__ == "__main__":
    pd.set_option('display.min_rows', 40)
initial_capital = 1 #Standard practice to make returns comparative and readable
def Create_Equity_Curve(data):
    equity_curve = pd.DataFrame(index = data.index)
    equity_curve['equity'] = data['Close'].ffill()
    equity_curve['Daily PnL(%)'] = (equity_curve['equity'].pct_change() * 100).fillna(0)
    equity_curve['Cumulative PnL(%)'] = ((1 + equity_curve['Daily PnL(%)']/100).cumprod() - 1).fillna(0)  
    equity_curve.index.name = 'date' 
    return equity_curve


#Creation of SVXY Unit Equity Curve Data
def Create_UnitDollar_Equity_Curve(data):
    equity_curve = pd.DataFrame(index = data.index)
    data_filled = data['Close'].ffill()
    equity_curve['Daily PnL(%)'] = (data_filled.pct_change() * 100).fillna(0)
    equity_curve['Growth Factor'] = 1 + (equity_curve['Daily PnL(%)'])/100
    equity_curve['Equity'] = initial_capital * equity_curve['Growth Factor'].cumprod()
    return equity_curve

Create_UnitDollar_SVXY_Equity_Curve = partial(Create_UnitDollar_Equity_Curve, data = SVXY_data)
Create_UnitDollar_SPY_Equity_Curve = partial(Create_UnitDollar_Equity_Curve, data = SPY_data)
SVXY_Unit_Equity_Curve = Create_UnitDollar_SVXY_Equity_Curve()
SPY_Unit_Equity_Curve = Create_UnitDollar_SPY_Equity_Curve()

def Plot_UnitDollar_SVXYvsSPY_Equity_Curve():
    fig, ax = plt.subplots(figsize = (16,8), dpi = 100)
    x = SVXY_Unit_Equity_Curve.index
    y = SVXY_Unit_Equity_Curve['Equity']
    x2 = SPY_Unit_Equity_Curve.index
    y2 = SPY_Unit_Equity_Curve['Equity']
    ax.plot(x,y, label = "SVXY (Strategy)", color = 'blue')
    ax.plot(x2,y2, label = "SPY (Benchmark)", color = 'purple')
    ax.grid(True, alpha = 0.3)
    ax.set_xlabel("Date", fontsize = 14)
    ax.set_ylabel("Equity Value", fontsize = 14)
    #ax.axvline(pd.Timestamp(2018,1,31), color = 'g', linestyle = '--')
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
    ax.axhline(y = 1, color = 'gray', linestyle = ':')

    #Breakeven Pointer
    ax.annotate("Breakeven Point", xy = (pd.Timestamp(2024,1,1), 1),
                xytext = (pd.Timestamp(2024,1,1), 1.7), fontsize = 12, color = 'black',
                ha = 'center', arrowprops=dict(facecolor = 'gray', arrowstyle = '-|>'))

    ax.legend()
    plt.title("SVXY Unit Equity Return vs SPY Unit Equity Return (Log Scale)", fontsize = 16, fontweight = 'bold')
    plt.show()


def Create_UnitDollar_Equity_Curve2(data):
    equity_curve = pd.DataFrame(index = data.index)
    data_filled = data['Close'].ffill()
    equity_curve['Daily PnL(%)'] = (data_filled.pct_change() * 100).fillna(0)
    return equity_curve
if __name__ == "__main__":
    print(Create_UnitDollar_Equity_Curve(data = SVXY_data))
    #print(Create_UnitDollar_SVXY_Equity_Curve()['Equity'].iloc[-1])







