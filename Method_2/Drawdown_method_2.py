import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
import numpy as np
from functools import partial
from create_equity_curve import create_equity_curve, create_unit_equity_curve
from average_recovery_func import recovery_period_list, underwater_period_list
distinct_trading_dates = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/dinstinct_trading_dates.csv', parse_dates=['Dates']).squeeze()
svxy_unit_equity_curve = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/SVXY Unit Equity Curve Data.csv', parse_dates=['date'])
spy_unit_equity_curve = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/SPY Unit Equity Curve Data.csv', parse_dates=['date'])
ss_strategy_unit_equity_curve = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/Short Strangle Unit Equity Curve Data.csv', parse_dates=['date'])

def Calculate_Drawdown(data):
    drawdown_data = pd.DataFrame()
    drawdown_data.index = data['date']
    running_max = data['equity'].cummax()
    drawdowns = (data['equity'] - running_max)/running_max * 100
    drawdown_data['Drawdown (%)'] = drawdowns.values
    return drawdown_data

def Calculate_Max_Drawdown_Pct(equity_data):
    drawdown_data = Calculate_Drawdown(equity_data)
    return drawdown_data['Drawdown (%)'].min()


#def calculate_drawdown_periods():
#    equity = 
short_strangle_equity_curve = create_equity_curve()
short_strangle_unit_equity_curve = create_unit_equity_curve()


short_strangle_equity_drawdown_data = Calculate_Drawdown(short_strangle_equity_curve)
short_strangle_unit_equity_drawdown_data = Calculate_Drawdown(short_strangle_unit_equity_curve)

#Both the equity_drawdown_data and the unit_equity_drawdown_data are going to be exactly the same
# I am doing this just for checking

spy_drawdown_data = Calculate_Drawdown(spy_unit_equity_curve)
svxy_drawdown_data = Calculate_Drawdown(svxy_unit_equity_curve)


def plot_drawdown(drawdown_data):
    x = drawdown_data.index
    y = drawdown_data['Drawdown (%)']
    data_copy = drawdown_data
    def give_distinct_drawdown(dd_data):
        return dd_data.loc[dd_data.index.isin(distinct_trading_dates)]
    y_distinct = give_distinct_drawdown(data_copy)['Drawdown (%)']
    #print(y_distinct)
    fig, ax = plt.subplots(figsize=(16, 8), dpi=100)
    ax.plot(x, y, label='Drawdown Curve', color='red', linewidth=3, zorder = 1)
    ax.axhline(y=0, color='gray', linestyle = '-', alpha = 0.7, zorder = 0)
    ax.fill_between(x,y, 0, where = (y < 0), color='red', alpha=0.3, label='Negative Drawdown Area', zorder = 2)
    ax.set_title('Drawdown Curve of Harvesting VRP via Short Strangles (Linear Scale)', fontsize=16, fontweight='bold')
    ax.set_xlabel('Date', fontsize=14, fontweight = 'bold')
    ax.set_ylabel('Drawdown (%)', fontsize=14, fontweight = 'bold')
    
    y_min = min(y)
    x_min = y.idxmin()
    average_drawdown = np.mean(y_distinct)
    median_drawdown = np.median(y_distinct)
    maximum_drawdown = y.min()
    ax.plot(x_min, y_min, 'ro', markersize=6, alpha = 0.8)
    plt.annotate(f'Max Drawdown Point',
                 xy=(x_min, y_min),
                 xytext=(pd.Timestamp(2019,1,1), y_min + 20),
                 arrowprops=dict(color = 'black', arrowstyle='->'),
                 fontsize=10, ha = 'right')
    
    #formatting of x-axis and y-axis labels
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100, decimals=2))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=2))

    #addition of statistics boxes:
    stats_text = f"""Statistics:\n{'-'*50}\nAvg DD: {average_drawdown:.2f}%\nMedian DD: {median_drawdown:.2f}%\nMax DD: {maximum_drawdown:.2f}%\n{'-'*50}\nAvg Recovery Period: {np.mean(recovery_period_list):.2f} days\nMed Recovery Period: {np.median(recovery_period_list):.2f} days\n{'-'*50}\nAvg DD Duration: {np.mean(underwater_period_list):.2f} days\nMed DD Duration: {np.median(underwater_period_list):.2f} days\n{'-'*50}\nTotal Completed Drawdowns: {len(recovery_period_list)}"""
    plt.text(pd.Timestamp(2011,8,1), -80, stats_text, bbox = dict(boxstyle = 'round, pad = 0.5', facecolor = 'pink', alpha = 0.4), alpha = 0.9, va = 'center',ha = 'left', fontsize = 8)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()

#from here
def plot_overlay_drawdown(data_a, data_b):
    """
    Alternative: Plot both drawdowns on the same chart for direct overlay comparison
    """
    fig, ax = plt.subplots(figsize=(16, 8), dpi=100)
    
    # Plot both series
    x_a = data_a.index
    y_a = data_a['Drawdown (%)']
    x_b = data_b.index
    y_b = data_b['Drawdown (%)']
    
    ax.plot(x_a, y_a, label='Short Strangle Strategy Drawdown', color='red', linewidth=2)
    if data_b.equals(spy_drawdown_data):
        ax.plot(x_b, y_b, label='SPY Drawdown', color='blue', linewidth=2)
    if data_b.equals(svxy_drawdown_data):
        ax.plot(x_b, y_b, label='SVXY Drawdown', color='blue', linewidth=2) 
    ax.axhline(y=0, color='gray', linestyle='-', alpha=0.7)
    #works for spy vs short strangle comparision
    if data_b.equals(spy_drawdown_data):
        ax.fill_between(x_a, y_a, 0, where=(y_a < 0), color='red', alpha=0.2)
        ax.fill_between(x_b, y_b, 0, where=(y_b < 0), color='blue', alpha=0.4)
    
    #works for svxy vs short strangle comparison
    if data_b.equals(svxy_drawdown_data):
        ax.fill_between(x_a, y_a, 0, where=(y_a < 0), color='red', alpha = 0.4)
        ax.fill_between(x_b, y_b, 0, where=(y_b < 0), color='blue', alpha = 0.2)

    
    if data_b.equals(spy_drawdown_data):
        ax.set_title('SPY vs Short Strangle Strategy Drawdown Comparison', fontsize=16, fontweight='bold')
    if data_b.equals(svxy_drawdown_data):
        ax.set_title('SVXY vs Short Strangle Strategy Drawdown Comparison', fontsize=16, fontweight='bold')
    ax.set_xlabel('Date', fontsize=14, fontweight = 'bold')
    ax.set_ylabel('Drawdown (%)', fontsize=14, fontweight = 'bold')

    """
    y_min_spy = min(y_a)
    x_min_spy = y_a.idxmin()
    y_min_svxy = min(y_b)
    x_min_svxy = y_b.idxmin()
    
    ax.plot(x_min_spy, y_min_spy, 'bo', markersize=8, alpha=0.8, label='SPY Max DD')
    ax.plot(x_min_svxy, y_min_svxy, 'ro', markersize=8, alpha=0.8, label='SVXY Max DD')
    ax.plot(vol_max_drawdown_date, vol_max_drawdown_val, 'go', markersize=8, alpha=0.8, label='Volmageddon')
    """
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100, decimals=1))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=2))
    
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()
if __name__ == "__main__":
    pd.set_option('display.min_rows',200)
    print(Calculate_Drawdown(short_strangle_equity_curve))
    #plot_drawdown(short_strangle_equity_drawdown_data)
    plot_overlay_drawdown(short_strangle_equity_drawdown_data, svxy_drawdown_data)
