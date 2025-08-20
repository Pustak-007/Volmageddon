import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
import numpy as np
from create_equity_curve import create_equity_curve, create_unit_equity_curve
from average_recovery_func import recovery_period_list, underwater_period_list

def Calculate_Drawdown(data):
    drawdown_data = pd.DataFrame()
    drawdown_data.index = data['date']
    running_max = data['equity'].cummax()
    drawdowns = (data['equity'] - running_max)/running_max * 100
    drawdown_data['Drawdown (%)'] = drawdowns.values
    return drawdown_data
#def calculate_drawdown_periods():
#    equity = 

equity_drawdown_data = Calculate_Drawdown(create_equity_curve())
unit_equity_drawdown_data = Calculate_Drawdown(create_unit_equity_curve())

def plot_drawdown(drawdown_data):
    x = drawdown_data.index
    y = drawdown_data['Drawdown (%)']
    fig, ax = plt.subplots(figsize=(16, 8), dpi=100)

    ax.plot(x, y, label='Drawdown Curve', color='red', linewidth=3, zorder = 1)
    ax.axhline(y=0, color='gray', linestyle = '-', alpha = 0.7, zorder = 0)
    ax.fill_between(x,y, 0, where = (y < 0), color='red', alpha=0.3, label='Negative Drawdown Area', zorder = 2)
    ax.set_title('Drawdown Curve of Harvesting VRP via Short Strangles (Linear Scale)', fontsize=16, fontweight='bold')
    ax.set_xlabel('Date', fontsize=14)
    ax.set_ylabel('Drawdown (%)', fontsize=14)
    
    y_min = min(y)
    x_min = y.idxmin()
    average_drawdown = np.mean(y)
    median_drawdown = np.median(y)
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
    stats_text = f"""Statistics:\n{'-'*50}\nAvg DD: {average_drawdown:.2f}%\nMedian DD: {median_drawdown:.2f}%\nMax DD: {maximum_drawdown:.2f}%\n{'-'*50}\nAvg Recovery Period: {np.mean(recovery_period_list):.2f} days\nMed Recovery Period: {np.median(recovery_period_list):.2f} days\n{'-'*50}\nAvg DD Duration: {np.mean(underwater_period_list):.2f} days\nMed DD Duration: {np.median(underwater_period_list):.2f} days"""
    plt.text(pd.Timestamp(2011,8,1), -80, stats_text, bbox = dict(boxstyle = 'round, pad = 0.5', facecolor = 'pink', alpha = 0.4), alpha = 0.9, va = 'center',ha = 'left', fontsize = 8)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()
if __name__ == "__main__":
    my_drawdown = equity_drawdown_data
    plot_drawdown(my_drawdown)
    #testing - the following code snippet is not relevant for the overall project
    large_press = 0
    if large_press == 1:
        print(my_drawdown)
        count = 0
        press = 1
        if press == 1:
            my_drawdown.to_csv("/Users/pustak/Downloads/my_drawdown.csv", index = False)
        rel_ser = equity_drawdown_data['Drawdown (%)']
        for i in range(1,len(rel_ser)):
            if (rel_ser.iloc[i] == 0 and rel_ser.iloc[i-1])!=0:
                count += 1
        print(count)