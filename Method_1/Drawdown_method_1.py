import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
from functools import partial
svxy_unit_equity_curve = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/SVXY Unit Equity Curve Data.csv', parse_dates=['date'])
spy_unit_equity_curve = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/SPY Unit Equity Curve Data.csv', parse_dates=['date'])
from average_recovery_func import recovery_period_list, underwater_period_list


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

give_spy_drawdown_data = partial(Calculate_Drawdown, spy_unit_equity_curve)
give_svxy_drawdown_data = partial(Calculate_Drawdown, svxy_unit_equity_curve)

spy_drawdown_data = give_spy_drawdown_data()
svxy_drawdown_data = give_svxy_drawdown_data()

def plot_drawdown(drawdown_data):
    x = drawdown_data.index
    y = drawdown_data['Drawdown (%)']
    fig, ax = plt.subplots(figsize=(16, 8), dpi=100)

    ax.plot(x, y, label='Drawdown Curve', color='red', linewidth=2, zorder = 1)
    ax.axhline(y=0, color='gray', linestyle = '-', alpha = 0.7, zorder = 0)
    ax.fill_between(x,y, 0, where = (y < 0), color='red', alpha=0.3, label='Negative Drawdown Area', zorder = 2)
    if drawdown_data.equals(spy_drawdown_data):
        ax.set_title('Drawdown Curve of SPY ETF', fontsize=16, fontweight='bold')
    if drawdown_data.equals(svxy_drawdown_data):
        ax.set_title('Drawdown Curve of SVXY ETF - Harvesting VRP via longing SVXY', fontsize = 16, fontweight = 'bold')
    ax.set_xlabel('Date', fontsize=14)
    ax.set_ylabel('Drawdown (%)', fontsize=14)
    
    y_min = min(y)
    x_min = y.idxmin()
    average_drawdown = np.mean(y)
    median_drawdown = np.median(y)
    maximum_drawdown = y.min()
    ax.plot(x_min, y_min, 'ro', markersize=6, alpha = 0.8)
    svxy_xytext_pos = (pd.Timestamp(2022,1,1), y_min - 3)
    spy_xytext_pos = (x_min - pd.Timedelta(days = 365*3), y_min + 10)
    plt.annotate(f'Max Drawdown Point',
                 xy=(x_min, y_min),
                 xytext=svxy_xytext_pos if drawdown_data.equals(svxy_drawdown_data) else spy_xytext_pos,
                 arrowprops=dict(color = 'black', arrowstyle='->'),
                 fontsize=10, va = 'center')
    
    #formatting of x-axis and y-axis labels
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100, decimals=2))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=2))

    #addition of statistics box
    stats_text = f"""Statistics:\n{'-'*50}\nAvg DD: {average_drawdown:.2f}%\nMedian DD: {median_drawdown:.2f}%\nMax DD: {maximum_drawdown:.2f}%\n{'-'*50}\nAvg Recovery Period: {np.mean(recovery_period_list):.2f} days\nMed Recovery Period: {np.median(recovery_period_list):.2f} days\n{'-'*50}\nAvg DD Duration: {np.mean(underwater_period_list):.2f} days\nMed DD Duration: {np.median(underwater_period_list):.2f} days\n{'-'*50}\nTotal Completed Drawdowns: {len(recovery_period_list)}"""
    if drawdown_data.equals(spy_drawdown_data): 
        plt.text(pd.Timestamp(2011,8,1), -30, stats_text, bbox = dict(boxstyle = 'round, pad = 0.5', facecolor = 'pink', alpha = 0.4), alpha = 0.9, va = 'center',ha = 'left', fontsize = 8)
    if drawdown_data.equals(svxy_drawdown_data):
        plt.text(pd.Timestamp(2011,8,1), -80, stats_text, bbox = dict(boxstyle = 'round, pad = 0.5', facecolor = 'pink', alpha = 0.4), alpha = 0.9, va = 'center',ha = 'left', fontsize = 8)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    plot_drawdown(svxy_drawdown_data)
