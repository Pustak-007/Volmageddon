import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
if __name__ == "__main__":
    pd.set_option('display.min_rows', 600)
df = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/Linearized_PnL.csv')
initial_capital = 10000
scaling_factor = round(initial_capital / 2313.4)
new_row = pd.DataFrame({'date' : [pd.Timestamp(2012,1,2)], 
                        'Daily PnL($)': [0.0], 
                        'Cumulative PnL($)': [0.0],
                        'equity':[initial_capital]})
#this makes sense because there is technically no relative pnl on the first day
#equity_curve where profit is scaled by 100 to make it representative of one option contract pair
# as premium is quoted on a per share basis, and option contracts are typically on 100 shares
def create_equity_curve():
    equity_df = pd.DataFrame()
    equity_df['date'] = pd.to_datetime(df['date'])
    equity_df['Daily PnL($)'] = df['daily_pnl'] * 100 * scaling_factor
    # mutliplied by 100 because the linearized pnl dataframe represents the pnl of holding one option - but one standard option contract contains 100 options
    equity_df['Cumulative PnL($)'] = equity_df['Daily PnL($)'].cumsum()
    equity_df['equity'] = initial_capital + equity_df['Daily PnL($)'].cumsum()
    equity_df = pd.concat([new_row, equity_df], ignore_index=True)
    equity_df['Daily PnL(%)'] = (equity_df['equity'].pct_change() * 100).fillna(0)
    equity_df['Cumulative PnL(%)'] = (1 + equity_df['Daily PnL(%)']/100).cumprod() - 1
    equity_df['Cumulative PnL(%)'] = (equity_df['Cumulative PnL(%)']*100).fillna(0)
    return equity_df
equity_df = create_equity_curve()
min_equity_val = equity_df['equity'].min()
max_equity_val = equity_df['equity'].max()
def create_unit_equity_curve():
    unit_equity_df = pd.DataFrame()
    unit_equity_df['date'] = equity_df['date'].copy()
    unit_equity_df['Daily PnL(%)'] = equity_df['Daily PnL(%)'].copy() 
    unit_equity_df['growth factor'] = (1 + unit_equity_df['Daily PnL(%)']/100)
    unit_equity_df['equity'] = 1 * unit_equity_df['growth factor'].cumprod()
    unit_equity_df['Cumulative PnL(%)'] = (1 + equity_df['Daily PnL(%)']/100).cumprod() - 1
    return unit_equity_df
unit_equity_df = create_unit_equity_curve()
min_unit_equity_val = unit_equity_df['equity'].min()
max_unit_equity_val = unit_equity_df['equity'].max()

def store_equity_curve():
    equity_df.to_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/Short Strangle Equity Curve Data.csv')
def store_unit_equity_curve():
    unit_equity_df.to_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/Short Strangle Unit Equity Curve Data.csv')

#Visualization
"""
def plot_equity_curve(equity_df):
    y = equity_df['equity']
    x = equity_df['date']
    fig, ax = plt.subplots(figsize=(16, 8), dpi = 100)
    ax.plot(x,y, label='Equity Curve', color='blue', linewidth=2)
    ax.set_xlabel('Date')
    ax.set_ylabel('Equity ($)')
    ax.set_title('Equity Curve Over Time', fontsize=16, fontweight='bold')
    ax.axhline(y = initial_capital, color='red', linestyle='--')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()
    plt.show()
plot_equity_curve(equity_df)
"""
def plot_equity_curve(equity_df):
    y = equity_df['equity']
    x = equity_df['date']

    fig, ax = plt.subplots(figsize=(16, 8), dpi=100)

    ax.plot(x, y, label='Equity Curve', color = 'blue', linewidth=2.5, alpha = 0.9)

    # Shade drawdown areas
    ax.fill_between(x, y, initial_capital, where=(y < initial_capital),
                    color='red', alpha=0.1, interpolate=True)
    #Shade areas above initial capital 
    ax.fill_between(x,y,initial_capital, where=(y > initial_capital), color = 'green', alpha = 0.1, interpolate=True)

    # Highlight initial capital
    ax.axhline(y=initial_capital, color='orange', linestyle='--', linewidth=1.5, label='Initial Capital')
    # X-axis formatting
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=2))
    plt.xticks(rotation=45, ha = 'right')

    # Labels & title
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Equity ($)', fontsize=12, fontweight='bold')
    ax.set_title('Equity Curve of Harvesting VRP via Short Strangles (Log Scale)', fontsize=18, fontweight='bold', pad=20)
    # Grid & legend
    ax.grid(True, linestyle='--', alpha=0.4)
    plt.yscale('log')   
    ax.set_yticks([10000, 15000, 20000, 25000, 30000, 35000])
    ax.set_yticklabels(['10,000', '15,000', '20,000', '25,000', '30,000', '35,000'])
    ax.axhline(y = min_equity_val, color = 'red', linestyle='--', linewidth=1.5, label='Volmageddon Low (Feb 2018)')
    ax.axhline(y = max_equity_val, color = 'green', linestyle='--', linewidth=1.5, label='Peak Equity')
    plt.tight_layout()
    ax.legend(fontsize=10)
    plt.show()


if __name__ == "__main__":
    print(equity_df)
    plot_equity_curve(equity_df)
    #yeah - as a means of safe-guard, always make sure to revert the press value back to zero
    # after the relevant data is properly stored.
    press = 0
    if press == 1:
        store_equity_curve()
        store_unit_equity_curve()

