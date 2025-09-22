import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FixedFormatter, FixedLocator, NullLocator

spy_unit_equity_curve = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/SPY Unit Equity Curve Data.csv', parse_dates=['date'])
short_strangle_unit_equity_curve = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/Short Strangle Unit Equity Curve Data.csv', parse_dates=['date'])

plt.figure(figsize=(16, 8))

plt.plot(short_strangle_unit_equity_curve['date'], short_strangle_unit_equity_curve['equity'],
         color='blue', linewidth=2, label='Short Strangle (Strategy)')
plt.plot(spy_unit_equity_curve['date'], spy_unit_equity_curve['equity'],
         color='purple', linewidth=2, label='SPY (Benchmark)')
ss_y_min = short_strangle_unit_equity_curve['equity'].min()
spy_y_max = spy_unit_equity_curve['equity'].max()
plt.yscale('log')
plt.axhline(y=1, color='gray', linestyle='--', alpha=0.7, label='Base Capital')

plt.title('Short Strangle Unit Equity Curve vs SPY Unit Equity Curve (Log Scale)',
          fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Date', fontsize=12, fontweight = 'bold')
plt.ylabel('Equity($)', fontsize=12, fontweight = 'bold' )

ax = plt.gca()
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=2))
y_ticks = [ss_y_min,0.5,1,2,spy_y_max,5,10]
plt.yticks(y_ticks)
ax.yaxis.set_major_locator(FixedLocator(y_ticks))
ax.yaxis.set_major_formatter(FixedFormatter([f'{tick:.2f}' for tick in y_ticks]))
ax.yaxis.set_minor_locator(NullLocator())

plt.axhline(y = ss_y_min, color = 'red', linestyle = '--', label = f'Minimum Value(Short Strangle): {round(ss_y_min,2)}')
plt.axhline(y = spy_y_max, color = 'green', linestyle = '--', label = f'Maximum Value(SPY): {round(spy_y_max,2)}')

plt.grid(True, alpha=0.3)
plt.legend(loc='lower left',bbox_to_anchor=(0,0.12))
plt.tight_layout()
plt.show()
