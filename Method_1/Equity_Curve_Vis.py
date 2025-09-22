import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.ticker import FixedFormatter, FixedLocator, NullLocator
import matplotlib.dates as mdates
from functools import partial

#Equity Curve Data
SVXY_Unit_Equity_Curve = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/SVXY Unit Equity Curve Data.csv')
SPY_Unit_Equity_Curve = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/SPY Unit Equity Curve Data.csv')

#Unit Equity Curve Data
SPY_Equity_Curve = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/SPY Equity Curve Data.csv')
SVXY_Equity_Curve = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/SVXY Equity Curve Data.csv')

def plot_unit_equity_curve(ticker):
    df = pd.read_csv(f'/Users/pustak/Desktop/Volmageddon/Local_Data/{ticker} Unit Equity Curve Data.csv', parse_dates=['date'])
    x = df['date']
    y = df['equity']
    fig, ax = plt.subplots(figsize = (16,8), dpi = 100)
    my_label = 'SPY (ETF) Benchmark' if ticker == 'SPY' else 'SVXY ETF'
    my_color = 'purple' if ticker == 'SPY' else 'blue'
    ax.plot(x,y, label = my_label , color = my_color)
    ax.grid(True, alpha = 0.3)
    ax.set_xlabel("Date", fontsize = 14, fontweight = 'bold')
    ax.set_ylabel("Equity Value ($)", fontsize = 14, fontweight = 'bold')
    ax.set_yscale('log')

    #manual_y_ticks
    if ticker == 'SPY':
        y_ticks = [1,2,3,4]
        ax.yaxis.set_major_locator(FixedLocator(y_ticks))
        ax.yaxis.set_major_formatter(FixedFormatter(y_ticks))
        ax.yaxis.set_minor_locator(NullLocator())
    if ticker == 'SVXY':
        y_ticks = [1,2,5,10,15,20,25]
        ax.yaxis.set_major_locator(FixedLocator(y_ticks))
        ax.yaxis.set_major_formatter(FixedFormatter(y_ticks))
        ax.yaxis.set_minor_locator(NullLocator())    
    if ticker == 'SVXY':
        # Volmageddon annotation (February 5, 2018)
        volmageddon_pointer_date = pd.Timestamp('2018-02-05')
        volmageddon_pointer_price = 5
        ax.annotate('Volmageddon\n(Feb 5, 2018)',
                    xy=(volmageddon_pointer_date, volmageddon_pointer_price),
                    xytext=(pd.Timestamp('2020-06-01'), 6),
                    fontsize=12,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor='red', alpha=0.7),
                    arrowprops=dict(arrowstyle='->', lw=2, color='red'))

        # COVID unwinding annotation (March 2020)
        covid_pointer_price = 2
        covid_pointer_date = pd.Timestamp(2020,3,22)
        ax.annotate('COVID Unwinding\n(March 2020)',
                    xy=(covid_pointer_date, covid_pointer_price),
                    xytext=(covid_pointer_date + pd.Timedelta(days = 60), 3),
                    fontsize=12,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor='orange', alpha=0.7),
                    arrowprops=dict(arrowstyle='->', lw=2, color='orange'))

    #China Shock annotation(August 2015)
    devalue_pointer_price = 6
    devalue_pointer_date = pd.Timestamp(2015,8,30)
    ax.annotate('Chinese Yuan\n Devaluation\n(August 2015)',
                xy = (devalue_pointer_date,devalue_pointer_price),
                xytext = (devalue_pointer_date + pd.Timedelta(days = 20), 13),
                fontsize = 12,
                bbox = dict(boxstyle = "round,pad=0.3", facecolor = 'purple', alpha = 0.7),
                arrowprops=dict(arrowstyle = '->', lw = 2, color = 'purple'))
    
    # X-axis formatting
    ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.axhline(y = 1, color = 'gray', linestyle = ':', label = 'Base Capital')
    #Breakeven Pointer
    ax.annotate("Breakeven Point", xy = (pd.Timestamp(2022,12,1), 1),
                xytext = (pd.Timestamp(2022,12,1), 1.4), fontsize = 12, color = 'black',
                ha = 'center', arrowprops=dict(facecolor = 'gray', arrowstyle = '-|>'))
    ax.legend()
    plt.title(f"{ticker} Unit Equity Curve (Log Scale)", fontsize = 16, fontweight = "bold")
    plt.show()

#plot benchmark vs svxy strategy unit equity curve    
def plot_SPYvsSVXY_Unit_Equity_Curve():
    spy_unit_equity = pd.read_csv( '/Users/pustak/Desktop/Volmageddon/Local_Data/SPY Unit Equity Curve Data.csv', parse_dates=['date'])
    svxy_unit_equity = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/SVXY Unit Equity Curve Data.csv', parse_dates=['date'])
    x1 = svxy_unit_equity['date']
    y1 = svxy_unit_equity['equity']
    x2 = spy_unit_equity['date']
    y2 = spy_unit_equity['equity']
    fig, ax = plt.subplots(figsize = (16,8), dpi = 100)
    ax.plot(x1,y1, label = "SVXY (Strategy)", color = 'blue')
    ax.plot(x2,y2, label = "SPY (Benchmark)", color = 'purple')
    ax.grid(True, alpha = 0.3)
    ax.set_xlabel("Date", fontsize = 14, fontweight = 'bold')
    ax.set_ylabel("Equity Value($)", fontsize = 14, fontweight = 'bold')
    #ax.axvline(pd.Timestamp(2018,1,31), color = 'g', linestyle = '--')
    ax.set_yscale('log')
    ax.axhline(y = 1, color = 'gray', linestyle = ':', label = 'Base Capital')

    #manual y_ticks
    y_ticks = [1,2,5,10,15,20,25]
    ax.yaxis.set_major_locator(FixedLocator(y_ticks))
    ax.yaxis.set_major_formatter(FixedFormatter(y_ticks))
    ax.yaxis.set_minor_locator(NullLocator())
    
    # X-axis formatting
    ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))


    #Breakeven Pointer
    ax.annotate("Breakeven Point", xy = (pd.Timestamp(2022,8,1), 1),
                xytext = (pd.Timestamp(2022,8,1), 1.4), fontsize = 12, color = 'black',
                ha = 'center', arrowprops=dict(facecolor = 'gray', arrowstyle = '-|>'))

    ax.legend()
    plt.title("SVXY Unit Equity Curve vs SPY Unit Equity Curve (Log Scale)", fontsize = 16, fontweight = 'bold')
    plt.show()

def plot_Method1vsMethod2_curve():
    spy_unit_equity = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/Short Strangle Unit Equity Curve Data.csv', parse_dates=['date'])
    svxy_unit_equity = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/SVXY Unit Equity Curve Data.csv', parse_dates=['date'])
    x1 = svxy_unit_equity['date']
    y1 = svxy_unit_equity['equity']
    x2 = spy_unit_equity['date']
    y2 = spy_unit_equity['equity']
    fig, ax = plt.subplots(figsize = (16,8), dpi = 100)
    ax.plot(x1,y1, label = "SVXY (Strategy)", color = 'blue')
    ax.plot(x2,y2, label = "SPY (Benchmark)", color = 'purple')
    ax.grid(True, alpha = 0.3)
    ax.set_xlabel("Date", fontsize = 14, fontweight = 'bold')
    ax.set_ylabel("Equity Value ($)", fontsize = 14, fontweight = 'bold')
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

plot_unit_equity_curve("SVXY")
                                  
