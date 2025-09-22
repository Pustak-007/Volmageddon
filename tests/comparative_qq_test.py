import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import probplot
from scipy.stats import norm

# Load data
svxy_unit_equity_curve = pd.read_csv(
    '/Users/pustak/Desktop/Volmageddon/Local_Data/SVXY Unit Equity Curve Data.csv',
    parse_dates=['date'], index_col=0)
spy_unit_equity_curve = pd.read_csv(
    '/Users/pustak/Desktop/Volmageddon/Local_Data/SPY Unit Equity Curve Data.csv',
    parse_dates=['date'], index_col=0)
ss_strategy_unit_equity_curve = pd.read_csv(
    '/Users/pustak/Desktop/Volmageddon/Local_Data/Short Strangle Unit Equity Curve Data.csv',
    parse_dates=['date'], index_col=0)
# Refining daily returns to remove 0-returns for weekends
spy_daily_returns = spy_unit_equity_curve[spy_unit_equity_curve['Daily PnL(%)'] != 0]['Daily PnL(%)']
svxy_daily_returns = svxy_unit_equity_curve[svxy_unit_equity_curve['Daily PnL(%)'] != 0]['Daily PnL(%)']
ss_strategy_daily_returns = ss_strategy_unit_equity_curve[ss_strategy_unit_equity_curve['Daily PnL(%)'] != 0]['Daily PnL(%)']


# Create figure with 2 QQ plots
fig, axes = plt.subplots(1,2, figsize=(16, 8), facecolor = 'white')
ax_svxy_qq, ax_ss_qq = axes

#SVXY QQ Plot
(osm, osr), (slope, intercept, r) = probplot(svxy_daily_returns, dist="norm")
ax_svxy_qq.scatter(osm, osr, s=15, alpha=0.6, label="Sample Quantiles")
ax_svxy_qq.plot(osm, slope * osm + intercept, 'r--', lw=2, label="Normal Line")
ax_svxy_qq.set_title("SVXY Daily Returns Distribution Q-Q Plot", fontweight='bold', fontsize=14)
ax_svxy_qq.set_xlabel("Theoretical Quantiles", fontweight = 'bold', fontsize = 12)
ax_svxy_qq.set_ylabel("Sample Quantiles", fontweight = 'bold', fontsize = 12)
ax_svxy_qq.legend()
ax_svxy_qq.grid(alpha=0.3)

#Short Strangle QQ Plot
(osm, osr), (slope, intercept, r) = probplot(ss_strategy_daily_returns, dist="norm")
ax_ss_qq.scatter(osm, osr, s=15, alpha=0.6, label="Sample Quantiles")
ax_ss_qq.plot(osm, slope * osm + intercept, 'r--', lw=2, label="Normal Line")
ax_ss_qq.set_title("Short Strangle Strategy Daily Returns Distribution  Q-Q Plot", fontweight='bold', fontsize=14)
ax_ss_qq.set_xlabel("Theoretical Quantiles", fontweight = 'bold', fontsize = 12)
ax_ss_qq.set_ylabel("Sample Quantiles", fontweight = 'bold', fontsize = 12)
ax_ss_qq.legend()
ax_ss_qq.grid(alpha=0.3)

plt.tight_layout(pad = 2)
pos1 = ax_svxy_qq.get_position()
right_edge_x = pos1.x1
separator_x = right_edge_x + 0.005
fig.add_artist(plt.Line2D([separator_x, separator_x], [0, 1],
                    transform=fig.transFigure,
                    color='gray', linewidth=2))
plt.show()


