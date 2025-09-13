import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
from functools import partial
svxy_unit_equity_curve = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/SVXY Unit Equity Curve Data.csv', parse_dates=['date'])
spy_unit_equity_curve = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/SPY Unit Equity Curve Data.csv', parse_dates=['date'])
from average_recovery_func import svxy_recovery_period_list, svxy_underwater_period_list, spy_recovery_period_list, spy_underwater_period_list


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

vol_check_df = svxy_drawdown_data.loc[pd.Timestamp(2018,1,1):pd.Timestamp(2018,6,1), 'Drawdown (%)'].to_frame(name = 'Drawdown (%)')
vol_max_drawdown_df = vol_check_df[vol_check_df['Drawdown (%)'] == vol_check_df['Drawdown (%)'].min()]
vol_max_drawdown_date = vol_max_drawdown_df.index
vol_max_drawdown_val = vol_max_drawdown_df['Drawdown (%)']

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
    
    svxy_xytext_pos = (pd.Timestamp(2022,1,1), y_min)
    spy_xytext_pos = (x_min - pd.Timedelta(days = 365*3), y_min + 10)
    svxy_xytext = ' (deceptive) \nMax Drawdown Point'
    svxy_xytext_2 = 'Volmageddon Drawdown (max)'
    spy_xytext = 'Max Drawdown Point'
    if drawdown_data.equals(svxy_drawdown_data):
        # Plot volmageddon max drawdown point
        ax.plot(vol_max_drawdown_date, vol_max_drawdown_val, 'bo', markersize=6, alpha = 0.8)
        
        plt.annotate(f'{svxy_xytext}',
                    xy=(x_min, y_min),
                    xytext=svxy_xytext_pos if drawdown_data.equals(svxy_drawdown_data) else spy_xytext_pos,
                    arrowprops=dict(color = 'black', arrowstyle='->'),
                    fontsize=10, va = 'center')
        plt.annotate(f'Volmageddon Drawdown (max)',
                     xy = (vol_max_drawdown_date[0], vol_max_drawdown_val.iloc[0]),
                     xytext=(pd.Timestamp(2016,9,1), -70),
                     arrowprops=dict(color = 'black', arrowstyle='->'),
                     fontsize=10, va = 'center', ha = 'center')
    
        
    elif drawdown_data.equals(spy_drawdown_data):
        plt.annotate(f'Max Drawdown Point',
                    xy=(x_min, y_min),
                    xytext=spy_xytext_pos,
                    arrowprops=dict(color = 'black', arrowstyle='->'),
                    fontsize=10, va = 'center')
    
    #formatting of x-axis and y-axis labels
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100, decimals=2))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=2))

    #addition of statistics box
    if drawdown_data.equals(spy_drawdown_data): 
        stats_text = f"""Statistics:\n{'-'*50}\nAvg DD: {average_drawdown:.2f}%\nMedian DD: {median_drawdown:.2f}%\nMax DD: {maximum_drawdown:.2f}%\n{'-'*50}\nAvg Recovery Period: {np.mean(spy_recovery_period_list):.2f} days\nMed Recovery Period: {np.median(spy_recovery_period_list):.2f} days\n{'-'*50}\nAvg DD Duration: {np.mean(spy_underwater_period_list):.2f} days\nMed DD Duration: {np.median(spy_underwater_period_list):.2f} days\n{'-'*50}\nTotal Completed Drawdowns: {len(spy_recovery_period_list)}"""
        plt.text(pd.Timestamp(2011,8,1), -30, stats_text, bbox = dict(boxstyle = 'round, pad = 0.5', facecolor = 'pink', alpha = 0.4), alpha = 0.9, va = 'center',ha = 'left', fontsize = 8)
    if drawdown_data.equals(svxy_drawdown_data):
        stats_text = f"""Statistics:\n{'-'*50}\nAvg DD: {average_drawdown:.2f}%\nMedian DD: {median_drawdown:.2f}%\nMax DD: {maximum_drawdown:.2f}%\nVol Max DD*: {vol_max_drawdown_val.iloc[0]:.2f}% \n{'-'*50}\nAvg Recovery Period: {np.mean(svxy_recovery_period_list):.2f} days\nMed Recovery Period: {np.median(svxy_recovery_period_list):.2f} days\n{'-'*50}\nAvg DD Duration: {np.mean(svxy_underwater_period_list):.2f} days\nMed DD Duration: {np.median(svxy_underwater_period_list):.2f} days\n{'-'*50}\nTotal Completed Drawdowns: {len(svxy_recovery_period_list)}"""
        plt.text(pd.Timestamp(2011,8,1), -80, stats_text, bbox = dict(boxstyle = 'round, pad = 0.5', facecolor = 'pink', alpha = 0.4), alpha = 0.9, va = 'center',ha = 'left', fontsize = 8)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()

#from here
def plot_comparison_drawdown(spy_drawdown_data, svxy_drawdown_data):
    """
    Plot both SPY and SVXY drawdowns in a shared subplot for easy comparison
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 8), dpi=100, sharex=True)
    
    # SVXY Plot (top)
    x_svxy = svxy_drawdown_data.index
    y_svxy = svxy_drawdown_data['Drawdown (%)']
    
    ax1.plot(x_svxy, y_svxy, label='SVXY Drawdown', color='red', linewidth=2, zorder=1)
    ax1.axhline(y=0, color='gray', linestyle='-', alpha=0.7, zorder=0)
    ax1.fill_between(x_svxy, y_svxy, 0, where=(y_svxy < 0), color='red', alpha=0.3, label='Negative Drawdown Area', zorder=2)
    
    ax1.set_title('SVXY ETF Drawdown Curve - Harvesting VRP via longing SVXY', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Drawdown (%)', fontsize=12)
    
    # Mark max drawdown and volmageddon for SVXY
    y_min_svxy = min(y_svxy)
    x_min_svxy = y_svxy.idxmin()
    ax1.plot(x_min_svxy, y_min_svxy, 'ro', markersize=6, alpha=0.8)
    ax1.plot(vol_max_drawdown_date, vol_max_drawdown_val, 'bo', markersize=6, alpha=0.8)
    
    # Annotations for SVXY
    ax1.annotate('Max DD (deceptive)', xy=(x_min_svxy, y_min_svxy), 
                xytext=(pd.Timestamp(2022,1,1), y_min_svxy), 
                arrowprops=dict(color='black', arrowstyle='->'), fontsize=9)
    ax1.annotate('Volmageddon Max DD', xy=(vol_max_drawdown_date[0], vol_max_drawdown_val.iloc[0]),
                xytext=(pd.Timestamp(2016,9,1), -70), 
                arrowprops=dict(color='black', arrowstyle='->'), fontsize=9, ha='center')
    
    # SPY Plot (bottom)
    x_spy = spy_drawdown_data.index
    y_spy = spy_drawdown_data['Drawdown (%)']
    
    ax2.plot(x_spy, y_spy, label='SPY Drawdown', color='blue', linewidth=2, zorder=1)
    ax2.axhline(y=0, color='gray', linestyle='-', alpha=0.7, zorder=0)
    ax2.fill_between(x_spy, y_spy, 0, where=(y_spy < 0), color='blue', alpha=0.3, label='Negative Drawdown Area', zorder=2)
    
    ax2.set_title('SPY ETF Drawdown Curve', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Date', fontsize=12)
    ax2.set_ylabel('Drawdown (%)', fontsize=12)
    
    # Mark max drawdown for SPY
    y_min_spy = min(y_spy)
    x_min_spy = y_spy.idxmin()
    ax2.plot(x_min_spy, y_min_spy, 'ro', markersize=6, alpha=0.8)
    
    # Annotation for SPY
    ax2.annotate('Max Drawdown Point', xy=(x_min_spy, y_min_spy),
                xytext=(x_min_spy - pd.Timedelta(days=365*3), y_min_spy + 5),
                arrowprops=dict(color='black', arrowstyle='->'), fontsize=9)
    
    # Formatting for both plots
    for ax in [ax1, ax2]:
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100, decimals=1))
        ax.grid(True, alpha=0.3)
        ax.legend(loc='lower right')
    
    # X-axis formatting (only on bottom plot since sharex=True)
    ax2.xaxis.set_major_locator(mdates.YearLocator())
    ax2.xaxis.set_minor_locator(mdates.MonthLocator(interval=3))
    
    # Add statistics boxes
    svxy_stats = f"""SVXY Statistics:
Avg DD: {np.mean(y_svxy):.2f}%
Max DD: {y_min_svxy:.2f}%
Vol Max DD: {vol_max_drawdown_val.iloc[0]:.2f}%"""
    
    spy_stats = f"""SPY Statistics:
Avg DD: {np.mean(y_spy):.2f}%
Max DD: {y_min_spy:.2f}%"""
    
    ax1.text(0.02, 0.05, svxy_stats, transform=ax1.transAxes, 
             bbox=dict(boxstyle='round,pad=0.3', facecolor='pink', alpha=0.7),
             fontsize=8, verticalalignment='bottom')
    
    ax2.text(0.02, 0.05, spy_stats, transform=ax2.transAxes,
             bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.7),
             fontsize=8, verticalalignment='bottom')
    
    plt.tight_layout()
    plt.show()

def plot_overlay_drawdown(spy_drawdown_data, svxy_drawdown_data):
    """
    Alternative: Plot both drawdowns on the same chart for direct overlay comparison
    """
    fig, ax = plt.subplots(figsize=(16, 8), dpi=100)
    
    # Plot both series
    x_spy = spy_drawdown_data.index
    y_spy = spy_drawdown_data['Drawdown (%)']
    x_svxy = svxy_drawdown_data.index
    y_svxy = svxy_drawdown_data['Drawdown (%)']
    
    ax.plot(x_spy, y_spy, label='SPY Drawdown', color='blue', linewidth=2)
    ax.plot(x_svxy, y_svxy, label='SVXY Drawdown', color='red', linewidth=2, alpha=0.6)
    
    ax.axhline(y=0, color='gray', linestyle='-', alpha=0.7)
    ax.fill_between(x_spy, y_spy, 0, where=(y_spy < 0), color='blue', alpha=0.4)
    ax.fill_between(x_svxy, y_svxy, 0, where=(y_svxy < 0), color='red', alpha=0.2)
    
    ax.set_title('SPY vs SVXY Drawdown Comparison', fontsize=16, fontweight='bold')
    ax.set_xlabel('Date', fontsize=14)
    ax.set_ylabel('Drawdown (%)', fontsize=14)

    """
    y_min_spy = min(y_spy)
    x_min_spy = y_spy.idxmin()
    y_min_svxy = min(y_svxy)
    x_min_svxy = y_svxy.idxmin()
    
    ax.plot(x_min_spy, y_min_spy, 'bo', markersize=8, alpha=0.8, label='SPY Max DD')
    ax.plot(x_min_svxy, y_min_svxy, 'ro', markersize=8, alpha=0.8, label='SVXY Max DD')
    ax.plot(vol_max_drawdown_date, vol_max_drawdown_val, 'go', markersize=8, alpha=0.8, label='Volmageddon')
    """
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100, decimals=1))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=3))
    
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()
#to here
if __name__ == "__main__":
    plot_spy_drawdown = partial(plot_drawdown, spy_drawdown_data)
    plot_svxy_drawdown = partial(plot_drawdown, svxy_drawdown_data)

    #plot_svxy_drawdown()
    plot_comparison_drawdown(spy_drawdown_data, svxy_drawdown_data)
    plot_overlay_drawdown(spy_drawdown_data, svxy_drawdown_data)
    #plot_spy_drawdown()

    #print(Calculate_Max_Drawdown_Pct(svxy_unit_equity_curve[(svxy_unit_equity_curve['date']>=pd.Timestamp(2018,1,1)) & (svxy_unit_equity_curve['date']<=pd.Timestamp(2018,2,28))]))
