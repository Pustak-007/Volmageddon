import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.ticker import FixedFormatter, FixedLocator, NullLocator
import matplotlib.dates as mdates

#Though the function is modular enough to accept any ticker with local equity curve data,
# but the annotations are specifically for SVXY
def plot_equity_curve(ticker):

    """
    df = pd.read_csv(f'/Users/pustak/Desktop/Volmageddon/Local_Data/{ticker} Unit Equity Curve Data.csv', parse_dates=['date'])
    x = df['date']
    y = df['equity']
    plt.plot(x,y)
    plt.yscale('log')
    plt.show()
    """

    fig, ax = plt.subplots(figsize=(16,8), dpi=100)
    df = pd.read_csv(f'/Users/pustak/Desktop/Volmageddon/Local_Data/{ticker} Equity Curve Data.csv', parse_dates=['date'])
    initial_equity_val = df.loc[df['date'] == pd.Timestamp(2012,1,2), 'equity'].iloc[0]
    x = df['date']
    y = df['equity']
    ax.plot(x, y, label='SVXY', linewidth=1.5, color='blue')
    ax.set_xlabel('Date', fontsize=14, fontweight = 'bold')
    ax.set_ylabel('Equity Value', fontsize=14, fontweight = 'bold')
    ax.set_yscale('log')
    # Volmageddon annotation (February 5, 2018)
    volmageddon_pointer_date = pd.Timestamp('2018-02-05')
    volmageddon_pointer_price = 140
    ax.annotate('Volmageddon\n(Feb 5, 2018)',
                xy=(volmageddon_pointer_date, volmageddon_pointer_price),
                xytext=(pd.Timestamp('2020-06-01'), 150),
                fontsize=12,
                bbox=dict(boxstyle="round,pad=0.3", facecolor='red', alpha=0.7),
                arrowprops=dict(arrowstyle='->', lw=2, color='red'))

    # COVID unwinding annotation (March 2020)
    covid_pointer_price = 25
    covid_pointer_date = pd.Timestamp(2020,3,22)
    ax.annotate('COVID Unwinding\n(March 2020)',
                xy=(covid_pointer_date, covid_pointer_price),
                xytext=(covid_pointer_date + pd.Timedelta(days = 60), 40),
                fontsize=12,
                bbox=dict(boxstyle="round,pad=0.3", facecolor='orange', alpha=0.7),
                arrowprops=dict(arrowstyle='->', lw=2, color='orange'))

    #China Shock annotation(August 2015)
    devalue_pointer_price = 70
    devalue_pointer_date = pd.Timestamp(2015,8,30)
    ax.annotate('Chinese Yuan\n Devaluation\n(August 2015)',
                xy = (devalue_pointer_date,devalue_pointer_price),
                xytext = (devalue_pointer_date + pd.Timedelta(days = 50), 150),
                fontsize = 12,
                bbox = dict(boxstyle = "round,pad=0.3", facecolor = 'purple', alpha = 0.7),
                arrowprops=dict(arrowstyle = '->', lw = 2, color = 'purple'))

    # Setting tick values manually - because logarithmic scale creates visualization
    # problems, better to standardize this practice -- because out of all the ones I have tried,
    # this is the one which works consistently
    ax.axhline(y = initial_equity_val, color = 'gray', linestyle = ':', label = 'initial equity')
    
    y_ticks = [10, initial_equity_val, 20, 30, 40, 50, 70, 100, 150, 200]
    ax.yaxis.set_major_locator(FixedLocator(y_ticks))
    ax.yaxis.set_major_formatter(FixedFormatter(y_ticks))
    ax.yaxis.set_minor_locator(NullLocator())

    # X-axis formatting
    ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    # Grid for better readability
    ax.grid(True, alpha=0.3)

    plt.title('SVXY Long (Buy & Hold) Strategy Equity Curve (Log Scale)', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.legend(fontsize=12)
    plt.show()
plot_equity_curve(ticker = 'SVXY')    