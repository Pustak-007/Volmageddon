import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd 
from create_equity_curve import equity_df, min_equity_val, max_equity_val, unit_equity_df, min_unit_equity_val, max_unit_equity_val
from matplotlib.ticker import FixedFormatter, FixedLocator, NullLocator

def plot_equity_curve(equity_df):
    y = equity_df['equity']
    x = equity_df['date']

    fig, ax = plt.subplots(figsize=(16, 8), dpi=100)

    ax.plot(x, y, label='Equity Curve', color = 'blue', linewidth=2.5, alpha = 0.9)
    initial_capital = equity_df['equity'].iloc[0]
    # Shade drawdown areas
    ax.fill_between(x, y, initial_capital, where=(y < initial_capital),
                    color='red', alpha=0.3, interpolate=True)
    #Shade areas above initial capital 
    ax.fill_between(x,y,initial_capital, where=(y > initial_capital), color = 'green', alpha = 0.2, interpolate=True)

    ax.axhline(y=initial_capital, color='orange', linestyle='--', linewidth=1.5, label='Initial Capital')
    # X-axis formatting
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=2))
    plt.xticks(rotation=45, ha = 'right')

    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Equity ($)', fontsize=12, fontweight='bold')
    ax.set_title('Equity Curve of Harvesting VRP via Short Strangles (Log Scale)', fontsize=18, fontweight='bold', pad=20)

    ax.grid(True, linestyle='--', alpha=0.4)
    plt.yscale('log')  
    if equity_df['equity'].iloc[0] == 10000: 
        y_ticks = [min_equity_val, 10000, 15000, 20000, 25000, 30000, max_equity_val]
        ax.yaxis.set_major_locator(FixedLocator(y_ticks))
        ax.yaxis.set_major_formatter(FixedFormatter([f'{tick:.2f}' for tick in y_ticks]))
        ax.yaxis.set_minor_locator(NullLocator())
        ax.axhline(y = min_equity_val, color = 'red', linestyle='--', linewidth=1.5, label='Trough Equity')
        ax.axhline(y = max_equity_val, color = 'green', linestyle='--', linewidth=1.5, label='Peak Equity')
    elif equity_df['equity'].iloc[0] == 1:
        y_ticks = [min_unit_equity_val, 1, 1.5, 2, 2.5, 3, max_unit_equity_val]
        ax.yaxis.set_major_locator(FixedLocator(y_ticks))
        ax.yaxis.set_major_formatter(FixedFormatter([f'{tick:.2f}' for tick in y_ticks]))
        ax.yaxis.set_minor_locator(NullLocator())
        ax.axhline(y = min_unit_equity_val, color = 'red', linestyle='--', linewidth=1.5, label='Trough Equity')
        ax.axhline(y = max_unit_equity_val, color = 'green', linestyle='--', linewidth=1.5, label='Peak Equity')
    plt.tight_layout()
    ax.legend(fontsize=10)   
    plt.show()

plot_equity_curve(equity_df=equity_df)

