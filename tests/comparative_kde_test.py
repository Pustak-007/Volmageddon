import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

# Load data
svxy_unit_equity_curve = pd.read_csv(
    '/Users/pustak/Desktop/Volmageddon/Local_Data/SVXY Unit Equity Curve Data.csv',
    parse_dates=['date'], index_col=0
)
spy_unit_equity_curve = pd.read_csv(
    '/Users/pustak/Desktop/Volmageddon/Local_Data/SPY Unit Equity Curve Data.csv',
    parse_dates=['date'], index_col=0
)
ss_strategy_unit_equity_curve = pd.read_csv(
    '/Users/pustak/Desktop/Volmageddon/Local_Data/Short Strangle Unit Equity Curve Data.csv',
    parse_dates=['date'], index_col=0
)

# Refining daily returns to remove 0-returns for weekends
spy_daily_returns = spy_unit_equity_curve[spy_unit_equity_curve['Daily PnL(%)'] != 0]['Daily PnL(%)']
svxy_daily_returns = svxy_unit_equity_curve[svxy_unit_equity_curve['Daily PnL(%)'] != 0]['Daily PnL(%)']
ss_strategy_daily_returns = ss_strategy_unit_equity_curve[ss_strategy_unit_equity_curve['Daily PnL(%)'] != 0]['Daily PnL(%)']

plt.figure(figsize=(16, 8))

sns.kdeplot(spy_daily_returns, label="SPY", linewidth=3)
sns.kdeplot(svxy_daily_returns, label="SVXY", linewidth=3)
sns.kdeplot(ss_strategy_daily_returns, label="Short Strangle", linewidth=3)

# Formatting
plt.title("KDE Comparison of Daily Returns", fontsize=16, fontweight="bold")
plt.xlabel("Daily Returns (%)", fontsize = 12, fontweight = 'bold')
plt.ylabel("Density", fontsize = 12, fontweight = 'bold')
plt.grid(alpha = 0.3)
plt.legend()
plt.tight_layout()

plt.show()
