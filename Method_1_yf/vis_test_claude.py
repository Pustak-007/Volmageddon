#This code is completely given my claude - but this definitely sets the standard
# for proper/appealing visualization - and what kind of information to display in the plot
# except just the graph.

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from Method1_data import SVXY_data
from SPY_data import SPY_data
from matplotlib.ticker import PercentFormatter
from functools import partial
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta

# Set style for better aesthetics
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

def Calculate_Drawdown(data):
    drawdown_data = pd.DataFrame()
    drawdown_data.index = data['Close'].index
    running_max = data['Close'].cummax()
    drawdowns = (data['Close'] - running_max)/running_max * 100
    drawdown_data['Drawdown (%)'] = drawdowns
    drawdown_data['Running Max'] = running_max
    drawdown_data['Close'] = data['Close']
    return drawdown_data

def Calculate_Max_Drawdown_Pct(data):
    return Calculate_Drawdown(data)['Drawdown (%)'].min()

def get_drawdown_stats(data):
    """Calculate comprehensive drawdown statistics"""
    dd_data = Calculate_Drawdown(data.ffill())
    dd_values = dd_data['Drawdown (%)']
    
    stats = {
        'max_drawdown': dd_values.min(),
        'avg_drawdown': dd_values[dd_values < 0].mean() if any(dd_values < 0) else 0,
        'recovery_time': calculate_recovery_times(dd_data),
        'drawdown_periods': count_drawdown_periods(dd_values)
    }
    return stats

def calculate_recovery_times(dd_data):
    """Calculate average recovery time from drawdowns"""
    dd_values = dd_data['Drawdown (%)']
    recovery_times = []
    in_drawdown = False
    start_dd = None
    
    for i, val in enumerate(dd_values):
        if val < -1 and not in_drawdown:  # Start of significant drawdown
            in_drawdown = True
            start_dd = i
        elif val >= -0.1 and in_drawdown:  # Recovery
            in_drawdown = False
            if start_dd is not None:
                recovery_times.append(i - start_dd)
    
    return np.mean(recovery_times) if recovery_times else 0

def count_drawdown_periods(dd_values):
    """Count number of significant drawdown periods"""
    count = 0
    in_drawdown = False
    
    for val in dd_values:
        if val < -5 and not in_drawdown:  # Significant drawdown threshold
            count += 1
            in_drawdown = True
        elif val >= -1 and in_drawdown:
            in_drawdown = False
    
    return count

def Plot_Enhanced_Drawdown(data, asset_name="Asset"):
    """Enhanced single asset drawdown plot"""
    drawdown_data = Calculate_Drawdown(data.ffill())
    stats = get_drawdown_stats(data)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12), dpi=120, 
                                   gridspec_kw={'height_ratios': [2, 1]})
    
    # Main drawdown plot
    x = drawdown_data.index
    y = drawdown_data['Drawdown (%)']
    
    # Create gradient fill
    ax1.fill_between(x, y, 0, where=(y <= 0), alpha=0.3, color='red', 
                     label='Drawdown Periods', interpolate=True)
    ax1.plot(x, y, linewidth=2, color='darkred', alpha=0.8, label='Drawdown %')
    
    # Highlight maximum drawdown
    max_dd_idx = y.idxmin()
    max_dd_val = y.min()
    ax1.scatter(max_dd_idx, max_dd_val, color='red', s=100, zorder=5, 
                label=f'Max DD: {max_dd_val:.2f}%')
    ax1.annotate(f'Max Drawdown\n{max_dd_val:.2f}%', 
                xy=(max_dd_idx, max_dd_val), 
                xytext=(10, 20), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='red', alpha=0.7),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    
    # Breakeven line with better styling
    ax1.axhline(y=0, color='gray', linestyle='--', alpha=0.7, linewidth=1)
    
    # Styling
    ax1.set_title(f'{asset_name} Drawdown Analysis - Enhanced View', 
                  fontsize=18, fontweight='bold', pad=20)
    ax1.set_ylabel('Drawdown (%)', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
    ax1.legend(loc='lower right', frameon=True, fancybox=True, shadow=True)
    ax1.yaxis.set_major_formatter(PercentFormatter(xmax=100, decimals=1))
    
    # Date formatting
    ax1.xaxis.set_major_locator(mdates.YearLocator())
    ax1.xaxis.set_minor_locator(mdates.MonthLocator(interval=3))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    
    # Add statistics box
    stats_text = f"""Statistics:
Max Drawdown: {stats['max_drawdown']:.2f}%
Avg Drawdown: {stats['avg_drawdown']:.2f}%
DD Periods: {stats['drawdown_periods']}
Avg Recovery: {stats['recovery_time']:.0f} days"""
    
    ax1.text(0.02, 0.02, stats_text, transform=ax1.transAxes, 
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8),
             verticalalignment='bottom', fontsize=10, fontfamily='monospace')
    
    # Underwater plot (bottom subplot)
    underwater = y.copy()
    underwater[underwater > 0] = 0
    
    bars = ax2.bar(x, underwater, width=1, color='red', alpha=0.6, 
                   label='Underwater Periods')
    
    ax2.set_ylabel('Underwater %', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Date', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.xaxis.set_major_locator(mdates.YearLocator())
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax2.yaxis.set_major_formatter(PercentFormatter(xmax=100, decimals=1))
    
    plt.tight_layout()
    plt.show()

def Plot_Enhanced_Comparison():
    """Enhanced comparison plot with multiple improvements"""
    drawdown_data_SVXY = Calculate_Drawdown(SVXY_data.ffill())
    drawdown_data_SPY = Calculate_Drawdown(SPY_data.ffill())
    
    svxy_stats = get_drawdown_stats(SVXY_data)
    spy_stats = get_drawdown_stats(SPY_data)
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 14), dpi=120)
    
    # Main comparison plot (top left)
    x_svxy = drawdown_data_SVXY.index
    y_svxy = drawdown_data_SVXY['Drawdown (%)']
    x_spy = drawdown_data_SPY.index
    y_spy = drawdown_data_SPY['Drawdown (%)']
    
    # Plot with gradient fills
    ax1.fill_between(x_svxy, y_svxy, 0, where=(y_svxy <= 0), alpha=0.3, 
                     color='red', label='SVXY Drawdown Periods')
    ax1.fill_between(x_spy, y_spy, 0, where=(y_spy <= 0), alpha=0.3, 
                     color='blue', label='SPY Drawdown Periods')
    
    ax1.plot(x_svxy, y_svxy, linewidth=2.5, color='darkred', 
             label=f'SVXY (Max DD: {svxy_stats["max_drawdown"]:.1f}%)', alpha=0.9)
    ax1.plot(x_spy, y_spy, linewidth=2.5, color='darkblue', 
             label=f'SPY (Max DD: {spy_stats["max_drawdown"]:.1f}%)', alpha=0.9)
    
    ax1.axhline(y=0, color='gray', linestyle='--', alpha=0.7)
    ax1.set_title('SVXY vs SPY: Drawdown Comparison', fontsize=16, fontweight='bold')
    ax1.set_ylabel('Drawdown (%)', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='lower right', frameon=True, fancybox=True, shadow=True)
    ax1.yaxis.set_major_formatter(PercentFormatter(xmax=100, decimals=1))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    
    # Rolling correlation (top right)
    # Align the data first
    common_dates = x_svxy.intersection(x_spy)
    svxy_aligned = y_svxy.reindex(common_dates)
    spy_aligned = y_spy.reindex(common_dates)
    
    rolling_corr = svxy_aligned.rolling(window=252).corr(spy_aligned)  # 1-year rolling correlation
    ax2.plot(common_dates, rolling_corr, color='purple', linewidth=2)
    ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.7)
    ax2.set_title('Rolling 1-Year Correlation (SVXY vs SPY Drawdowns)', fontsize=16, fontweight='bold')
    ax2.set_ylabel('Correlation', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    
    # Drawdown distribution histogram (bottom left)
    svxy_dd_values = y_svxy[y_svxy < 0]
    spy_dd_values = y_spy[y_spy < 0]
    
    ax3.hist(svxy_dd_values, bins=30, alpha=0.7, color='red', label='SVXY', density=True)
    ax3.hist(spy_dd_values, bins=30, alpha=0.7, color='blue', label='SPY', density=True)
    ax3.axvline(svxy_stats['max_drawdown'], color='darkred', linestyle='--', 
                label=f'SVXY Max: {svxy_stats["max_drawdown"]:.1f}%')
    ax3.axvline(spy_stats['max_drawdown'], color='darkblue', linestyle='--', 
                label=f'SPY Max: {spy_stats["max_drawdown"]:.1f}%')
    
    ax3.set_title('Drawdown Distribution', fontsize=16, fontweight='bold')
    ax3.set_xlabel('Drawdown (%)', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Density', fontsize=12, fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Statistics comparison table (bottom right)
    ax4.axis('off')
    
    comparison_data = {
        'Metric': ['Max Drawdown (%)', 'Avg Drawdown (%)', 'DD Periods', 'Avg Recovery (days)'],
        'SVXY': [f"{svxy_stats['max_drawdown']:.2f}", 
                 f"{svxy_stats['avg_drawdown']:.2f}",
                 f"{svxy_stats['drawdown_periods']}", 
                 f"{svxy_stats['recovery_time']:.0f}"],
        'SPY': [f"{spy_stats['max_drawdown']:.2f}", 
                f"{spy_stats['avg_drawdown']:.2f}",
                f"{spy_stats['drawdown_periods']}", 
                f"{spy_stats['recovery_time']:.0f}"]
    }
    
    table = ax4.table(cellText=[[comparison_data['Metric'][i], 
                                comparison_data['SVXY'][i], 
                                comparison_data['SPY'][i]] 
                               for i in range(len(comparison_data['Metric']))],
                     colLabels=['Metric', 'SVXY', 'SPY'],
                     cellLoc='center',
                     loc='center',
                     colWidths=[0.4, 0.3, 0.3])
    
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 2)
    
    # Style the table
    for i in range(len(comparison_data['Metric']) + 1):
        for j in range(3):
            if i == 0:  # Header row
                table[(i, j)].set_facecolor('#4472C4')
                table[(i, j)].set_text_props(weight='bold', color='white')
            else:
                if j == 1:  # SVXY column
                    table[(i, j)].set_facecolor('#FFE6E6')
                elif j == 2:  # SPY column
                    table[(i, j)].set_facecolor('#E6F3FF')
                else:  # Metric column
                    table[(i, j)].set_facecolor('#F0F0F0')
    
    ax4.set_title('Statistical Comparison', fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.show()

def Plot_Risk_Adjusted_View():
    """Additional risk-adjusted visualization"""
    drawdown_data_SVXY = Calculate_Drawdown(SVXY_data.ffill())
    drawdown_data_SPY = Calculate_Drawdown(SPY_data.ffill())
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8), dpi=120)
    
    # Drawdown vs Time scatter (left)
    svxy_dd = drawdown_data_SVXY['Drawdown (%)']
    spy_dd = drawdown_data_SPY['Drawdown (%)']
    
    # Convert dates to numbers for scatter plot
    svxy_dates_num = mdates.date2num(drawdown_data_SVXY.index)
    spy_dates_num = mdates.date2num(drawdown_data_SPY.index)
    
    scatter1 = ax1.scatter(svxy_dates_num, svxy_dd, alpha=0.6, c=svxy_dd, 
                          cmap='Reds_r', s=20, label='SVXY')
    scatter2 = ax1.scatter(spy_dates_num, spy_dd, alpha=0.6, c=spy_dd, 
                          cmap='Blues_r', s=20, label='SPY', marker='^')
    
    ax1.axhline(y=0, color='gray', linestyle='--', alpha=0.7)
    ax1.set_title('Drawdown Intensity Over Time', fontsize=16, fontweight='bold')
    ax1.set_ylabel('Drawdown (%)', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Max drawdown by year (right)
    svxy_yearly_max = svxy_dd.groupby(svxy_dd.index.year).min()
    spy_yearly_max = spy_dd.groupby(spy_dd.index.year).min()
    
    years = svxy_yearly_max.index
    x_pos = np.arange(len(years))
    width = 0.35
    
    bars1 = ax2.bar(x_pos - width/2, svxy_yearly_max.values, width, 
                    label='SVXY', color='red', alpha=0.7)
    bars2 = ax2.bar(x_pos + width/2, spy_yearly_max.values, width, 
                    label='SPY', color='blue', alpha=0.7)
    
    ax2.set_title('Annual Maximum Drawdowns', fontsize=16, fontweight='bold')
    ax2.set_ylabel('Max Drawdown (%)', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(years, rotation=45)
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.yaxis.set_major_formatter(PercentFormatter(xmax=100, decimals=1))
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax2.annotate(f'{height:.1f}%', xy=(bar.get_x() + bar.get_width()/2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom',
                    fontsize=8, rotation=0)
    
    for bar in bars2:
        height = bar.get_height()
        ax2.annotate(f'{height:.1f}%', xy=(bar.get_x() + bar.get_width()/2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom',
                    fontsize=8, rotation=0)
    
    plt.tight_layout()
    plt.show()

# Create partial functions for easier use
SVXY_Drawdown_Data = Calculate_Drawdown(data=SVXY_data.ffill())
SPY_Drawdown_Data = Calculate_Drawdown(data=SPY_data.ffill())

Plot_Enhanced_SVXY_Drawdown = partial(Plot_Enhanced_Drawdown, data=SVXY_data, asset_name="SVXY VRP Strategy")
Plot_Enhanced_SPY_Drawdown = partial(Plot_Enhanced_Drawdown, data=SPY_data, asset_name="SPY")

if __name__ == "__main__":
    # Run all enhanced visualizations
    print("Generating Enhanced Drawdown Visualizations...")
    
    # Individual enhanced plots
    Plot_Enhanced_SVXY_Drawdown()
    Plot_Enhanced_SPY_Drawdown()
    
    # Enhanced comparison
    Plot_Enhanced_Comparison()
    
    # Risk-adjusted view
    Plot_Risk_Adjusted_View()
    
    print("All visualizations generated successfully!")