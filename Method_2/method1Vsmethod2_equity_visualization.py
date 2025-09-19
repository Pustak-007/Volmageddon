import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FixedFormatter, FixedLocator, NullLocator

spy_unit_equity_curve = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/SPY Unit Equity Curve Data.csv', parse_dates=['date'])
short_strangle_unit_equity_curve = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/Short Strangle Unit Equity Curve Data.csv', parse_dates=['date'])
svxy_unit_equity_curve = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/SVXY Unit Equity Curve Data.csv', parse_dates=['date'])

fig, ax = plt.subplots(figsize=(16,8), dpi=100)
svxy_max = svxy_unit_equity_curve['equity'].max()
short_strangle_min = short_strangle_unit_equity_curve['equity'].min()
ax.plot(short_strangle_unit_equity_curve['date'], short_strangle_unit_equity_curve['equity'],
        color='blue', linewidth=2, label='SPY Short Strangle Strategy')
ax.plot(svxy_unit_equity_curve['date'], svxy_unit_equity_curve['equity'],
        color='purple', linewidth=2, label='SVXY ETF')
ax.axhline(y=1, color='gray', linestyle='--', alpha=0.7, label='Base Capital')
ax.axhline(y=svxy_max, color='green', linestyle='--', alpha=0.7, label='Maximum Value (SVXY)')
ax.axhline(y=round(short_strangle_min,2), color='red', linestyle='--', alpha=0.7, label='Minimum Value (Short Strangle)')

ax.set_xlabel('Date', fontsize=12, fontweight = 'bold')
ax.set_ylabel('Equity($)', fontsize=12, fontweight = 'bold' )
ax.set_yscale('log')
#manual y_ticks
y_ticks = [round(short_strangle_min,2),0.5,1,2,5,10,15,20,25]
ax.yaxis.set_major_locator(FixedLocator(y_ticks))
ax.yaxis.set_major_formatter(FixedFormatter(y_ticks))
ax.yaxis.set_minor_locator(NullLocator())

# X-axis formatting
ax.xaxis.set_major_locator(mdates.YearLocator(1))
ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

ax.set_title('SPY Short Strangle Unit Equity Curve vs SVXY Unit Equity Curve (Log Scale)', fontsize = 16, fontweight = 'bold')
ax.grid(alpha = 0.3)

ax.legend(loc = 'best')

plt.show()
