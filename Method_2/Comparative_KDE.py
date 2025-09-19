import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from scipy.stats import norm

def generate_analysis_text(daily_returns, name):
    mean = daily_returns.mean()
    stdev = daily_returns.std()
    skewness = daily_returns.skew()
    kurt = daily_returns.kurt()
    median = daily_returns.median()
    min_val = daily_returns.min()
    max_val = daily_returns.max()

    stats_text = f"""{name} Statistical Summary
{'-'*30}
Mean: {mean:15.3f}%
Median: {median:13.3f}%
Std Dev: {stdev:12.3f}%
Min / Max: {min_val:.2f}% / {max_val:.2f}%
Skewness: {skewness:11.3f}
Kurtosis: {kurt:11.3f}"""

    lower_threshold = mean - 2 * stdev
    upper_threshold = mean + 2 * stdev

    prob_normal_negative = norm.cdf(lower_threshold, loc=mean, scale=stdev)
    prob_actual_negative = (daily_returns < lower_threshold).sum() / len(daily_returns)
    prob_normal_positive = 1 - norm.cdf(upper_threshold, loc=mean, scale=stdev)
    prob_actual_positive = (daily_returns > upper_threshold).sum() / len(daily_returns)
    prob_normal_total = prob_normal_negative + prob_normal_positive
    prob_actual_total = prob_actual_negative + prob_actual_positive

    prob_text = f"""
{name} Tail Probability Analysis (Beyond 2σ)
{'-'*45}
                 {'Actual':>10s} {'Normal':>10s}
{'Total Outlier:':<15} {prob_actual_total:>9.2%} {prob_normal_total:>10.2%}
{'Negative Tail:':<15} {prob_actual_negative:>9.2%} {prob_normal_negative:>10.2%}
{'Positive Tail:':<15} {prob_actual_positive:>9.2%} {prob_normal_positive:>10.2%}"""

    return f"{stats_text}\n{prob_text}"


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

spy_daily_returns = spy_unit_equity_curve[spy_unit_equity_curve['Daily PnL(%)'] != 0]['Daily PnL(%)']
svxy_daily_returns = svxy_unit_equity_curve[svxy_unit_equity_curve['Daily PnL(%)'] != 0]['Daily PnL(%)']
ss_strategy_daily_returns = ss_strategy_unit_equity_curve[ss_strategy_unit_equity_curve['Daily PnL(%)'] != 0]['Daily PnL(%)']

fig, ax = plt.subplots(figsize=(16, 8))

sns.kdeplot(spy_daily_returns, label="SPY", lw=3)
sns.kdeplot(svxy_daily_returns, label="SVXY", lw=3)
sns.kdeplot(ss_strategy_daily_returns, label="Short Strangle", lw=3)

spy_analysis_text = generate_analysis_text(spy_daily_returns, "SPY")
ss_analysis_text = generate_analysis_text(ss_strategy_daily_returns, "Short Strangle")
svxy_analysis_text = generate_analysis_text(svxy_daily_returns, "SVXY")

props = dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.9)

ax.text(0.02, 0.98, spy_analysis_text, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props, fontfamily='monospace')
ax.text(0.32, 0.68, ss_analysis_text, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props, fontfamily='monospace')
ax.text(0.02, 0.52, svxy_analysis_text, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props, fontfamily='monospace')

ax.set_title("KDE Comparison of Daily Returns with Statistical & Tail Analysis", fontsize=16, fontweight="bold")
ax.set_xlabel("Daily Returns (%)", fontsize=12, fontweight='bold')
ax.set_ylabel("Density", fontsize=12, fontweight='bold')
ax.grid(alpha=0.3)
ax.legend(loc='upper right', fontsize=12)
ax.set_xlim(svxy_daily_returns.min() - 5, svxy_daily_returns.max() + 5)
ax.set_ylim(bottom=0)

plt.tight_layout()
plt.show()