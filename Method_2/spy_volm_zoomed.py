import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import NullLocator
import matplotlib.dates as mdates
# Load data
volm_begin_date = pd.Timestamp(2018,2,1)
volm_end_date = pd.Timestamp(2018,2,28)
spy_unit_equity_curve = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/SPY Unit Equity Curve Data.csv', parse_dates=['date'], index_col=0)

# Mask for the zoomed-in period
zoom_in_mask = (spy_unit_equity_curve['date'] >= volm_begin_date) & \
               (spy_unit_equity_curve['date'] <= volm_end_date)
spy_unit_equity_curve_zoomed_in = spy_unit_equity_curve[zoom_in_mask]

#distinguish relevant data
spy_volm_begin_equity = spy_unit_equity_curve_zoomed_in[spy_unit_equity_curve_zoomed_in['date'] == volm_begin_date].iloc[0]['equity']
spy_volm_end_equity = spy_unit_equity_curve_zoomed_in[spy_unit_equity_curve_zoomed_in['date'] == volm_end_date].iloc[0]['equity']
print(spy_volm_begin_equity)
print(spy_volm_end_equity)
# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 8), sharex=False)

# Full equity curve with highlighted period
ax1.plot(spy_unit_equity_curve['date'], spy_unit_equity_curve['equity'], color='gray', label='Full Equity Curve')
ax1.plot(spy_unit_equity_curve_zoomed_in['date'], spy_unit_equity_curve_zoomed_in['equity'], color='red', label='Feb 2018 Highlight')
ax1.set_yscale('log')
ax1.set_title('Full SPY Unit Equity Curve with Highlighted Volmageddon Regime', fontsize = 16, fontweight = 'bold')
ax1.set_yticks([1,2,3,4])
ax1.set_yticklabels(['1','2','3','4'])
ax1.yaxis.set_minor_locator(NullLocator())
ax1.set_ylabel('Equity ($)', fontsize = 12, fontweight = 'bold')
ax1.legend()
ax1.grid(True)
# X-axis formatting
ax1.xaxis.set_major_locator(mdates.YearLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax1.xaxis.set_minor_locator(mdates.MonthLocator(interval=2))
# Zoomed-in view
ax2.plot(spy_unit_equity_curve_zoomed_in['date'], spy_unit_equity_curve_zoomed_in['equity'], color='red', label='Feb 2018 Zoom')
ax2.set_yscale('log')
y_ticks = [2.05,2.1,2.1645417529880535,2.2,2.243665258964149]
y_ticks2 = [2.05,2.1,2.165,2.2]
ax2.set_yticks(y_ticks)
ax2.set_yticklabels(list(map(str,y_ticks2)) + ['2.244'])
ax2.yaxis.set_minor_locator(NullLocator())
ax2.axhline(y = spy_volm_begin_equity, color = 'green', linestyle = '--', label = f'Begin Value: {round(spy_volm_begin_equity,3)}')
ax2.axhline(y = spy_volm_end_equity, color = 'red', linestyle = '--', label = f'End Value: {round(spy_volm_end_equity,3)}')
ax2.set_ylabel('Equity ($)', fontsize = 12, fontweight = 'bold')
ax2.set_title('Zoomed-In SPY Unit Equity Curve (Feb 2018)', fontsize = 14, fontweight = 'bold')
ax2.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
