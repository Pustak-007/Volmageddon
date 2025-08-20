#This whole code is fully designed by AI.

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Set matplotlib style for better aesthetics
plt.rcParams['figure.facecolor'] = '#F8F9FA'
plt.rcParams['axes.facecolor'] = '#FFFFFF'
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.color'] = '#E5E5E5'
plt.rcParams['grid.linewidth'] = 0.5

if __name__ == "__main__":
    pd.set_option('display.min_rows', 600)
    
    # Load and process data
    df = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/Linearized_PnL.csv')
    initial_capital = 10000
    multiplier = round(initial_capital / 2313.4)
    
    new_row = pd.DataFrame({'date': [pd.Timestamp(2012, 1, 2)], 
                           'daily_pnl': [0.0], 
                           'cumulative_pnl': [0.0],
                           'equity': [initial_capital]})
    
    # Create equity dataframe
    equity_df = pd.DataFrame()
    equity_df['date'] = pd.to_datetime(df['date'])
    equity_df['daily_pnl'] = df['daily_pnl'] * 100 * multiplier
    equity_df['cumulative_pnl'] = equity_df['daily_pnl'].cumsum()
    equity_df['equity'] = initial_capital + equity_df['daily_pnl'].cumsum()
    equity_df = pd.concat([new_row, equity_df], ignore_index=True)
    equity_df['daily_returns'] = equity_df['equity'].pct_change().fillna(0)
    equity_df['cumulative_returns'] = (1 + equity_df['daily_returns']).cumprod() - 1
    equity_df['cumulative_returns'] = equity_df['cumulative_returns'].fillna(0)
    
    # Calculate additional metrics
    total_return = (equity_df['equity'].iloc[-1] / initial_capital - 1) * 100
    max_equity = equity_df['equity'].max()
    min_equity = equity_df['equity'].min()
    max_drawdown = ((equity_df['equity'].cummax() - equity_df['equity']) / equity_df['equity'].cummax()).max() * 100
    
    # Create the enhanced visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12), gridspec_kw={'height_ratios': [3, 1]})
    fig.suptitle('Portfolio Equity Curve Analysis\nVolatility Trading Strategy Performance', 
                 fontsize=16, fontweight='bold', y=0.95)
    
    # Main equity curve with enhanced styling
    ax1.plot(equity_df['date'], equity_df['equity'], linewidth=3, color='#1f77b4', 
             label='Equity Curve', zorder=3)
    
    # Reference lines
    ax1.axhline(y=initial_capital, color='#d62728', linestyle='--', alpha=0.8, 
                linewidth=2, label=f'Initial Capital (${initial_capital:,})', zorder=2)
    ax1.axhline(y=max_equity, color='#ff7f0e', linestyle=':', alpha=0.8, 
                linewidth=2, label=f'Peak (${max_equity:,.0f})', zorder=2)
    
    # Fill areas for visual appeal
    ax1.fill_between(equity_df['date'], equity_df['equity'], initial_capital, 
                     where=(equity_df['equity'] >= initial_capital), alpha=0.2, 
                     color='#2ca02c', interpolate=True, label='Profit Zone')
    ax1.fill_between(equity_df['date'], equity_df['equity'], initial_capital, 
                     where=(equity_df['equity'] < initial_capital), alpha=0.2, 
                     color='#d62728', interpolate=True, label='Loss Zone')
    
    # Formatting main plot
    ax1.set_ylabel('Portfolio Value ($)', fontsize=12, fontweight='bold')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    ax1.grid(True, alpha=0.6, linestyle='-', linewidth=0.5)
    ax1.legend(loc='upper left', frameon=True, fancybox=True, shadow=True, 
               fontsize=10, framealpha=0.9)
    
    # Enhanced spines
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_linewidth(1.2)
    ax1.spines['bottom'].set_linewidth(1.2)
    
    # Format x-axis for main plot
    ax1.xaxis.set_major_locator(mdates.YearLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax1.xaxis.set_minor_locator(mdates.MonthLocator((1, 7)))
    ax1.tick_params(axis='both', which='major', labelsize=10)
    
    # Daily returns subplot with custom colors
    positive_mask = equity_df['daily_returns'] >= 0
    ax2.bar(equity_df['date'][positive_mask], equity_df['daily_returns'][positive_mask] * 100, 
            color='#2ca02c', alpha=0.7, width=1, label='Positive Returns')
    ax2.bar(equity_df['date'][~positive_mask], equity_df['daily_returns'][~positive_mask] * 100, 
            color='#d62728', alpha=0.7, width=1, label='Negative Returns')
    
    ax2.set_ylabel('Daily Return (%)', fontsize=11, fontweight='bold')
    ax2.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.8, linewidth=1)
    ax2.grid(True, alpha=0.6, linestyle='-', linewidth=0.5)
    ax2.legend(loc='upper right', fontsize=9)
    
    # Enhanced spines for subplot
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_linewidth(1.2)
    ax2.spines['bottom'].set_linewidth(1.2)
    
    # Format x-axis for subplot
    ax2.xaxis.set_major_locator(mdates.YearLocator())
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax2.tick_params(axis='both', which='major', labelsize=10)
    
    # Add performance statistics text box
    stats_text = f"""Performance Statistics:
Total Return: {total_return:.1f}%
Max Drawdown: {max_drawdown:.1f}%
Final Value: ${equity_df['equity'].iloc[-1]:,.0f}
Peak Value: ${max_equity:,.0f}
Trough Value: ${min_equity:,.0f}
Multiplier: {multiplier}x"""
    
    # Custom text box styling
    props = dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.8, 
                 edgecolor='navy', linewidth=1.5)
    ax1.text(0.02, 0.98, stats_text, transform=ax1.transAxes, fontsize=10,
             verticalalignment='top', bbox=props, fontfamily='monospace',
             fontweight='bold')
    
    # Adjust layout and display
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.25, top=0.92)
    
    # Add a subtle background color
    fig.patch.set_facecolor('#F8F9FA')
    
    plt.show()
    
    # Print summary statistics
    print("\n" + "="*60)
    print("PORTFOLIO PERFORMANCE SUMMARY")
    print("="*60)
    print(f"Initial Capital: ${initial_capital:,}")
    print(f"Final Value: ${equity_df['equity'].iloc[-1]:,.0f}")
    print(f"Total Return: {total_return:.2f}%")
    print(f"Maximum Value: ${max_equity:,.0f}")
    print(f"Minimum Value: ${min_equity:,.0f}")
    print(f"Maximum Drawdown: {max_drawdown:.2f}%")
    print(f"Strategy went negative: {any(num < 0 for num in equity_df['equity'])}")
    print(f"Contract Multiplier: {multiplier}x")
    print("="*60)