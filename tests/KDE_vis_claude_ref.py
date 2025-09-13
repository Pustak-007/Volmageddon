"""from scipy.stats import norm
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

equity_curve = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/Short Strangle Unit Equity Curve Data.csv', index_col = 0)
daily_returns_df = equity_curve[equity_curve['Daily PnL(%)']!=0]
daily_returns = daily_returns_df['Daily PnL(%)']
mean = daily_returns.mean()
stdev = daily_returns.std()
sns.kdeplot(x = daily_returns.values, fill = True, color = 'darkblue', lw = 3)
x_range = np.linspace(daily_returns.min(), daily_returns.max(), 1000)
normal = norm.pdf(x_range, loc = mean, scale = stdev)
plt.plot(x_range, normal, lw = 3)
plt.show()
"""
#This is just for reference - fully designed by claude - not applicable
from scipy.stats import norm, jarque_bera, skew, kurtosis
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Load and process data
equity_curve = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/Short Strangle Unit Equity Curve Data.csv', index_col=0)
daily_returns_df = equity_curve[equity_curve['Daily PnL(%)'] != 0]
daily_returns = daily_returns_df['Daily PnL(%)']

# Calculate statistics
mean = daily_returns.mean()
stdev = daily_returns.std()
skewness = skew(daily_returns)
kurt = kurtosis(daily_returns)
jb_stat, jb_pvalue = jarque_bera(daily_returns)

# Set up the plot with better styling
plt.style.use('seaborn-v0_8-whitegrid')  # Modern clean style
fig, ax = plt.subplots(figsize=(12, 8))

# Create the KDE plot with gradient-like effect
sns.kdeplot(x=daily_returns.values, fill=True, color='steelblue', 
           alpha=0.7, linewidth=0, ax=ax, label='Actual Distribution')

# Add a subtle outline to the KDE
sns.kdeplot(x=daily_returns.values, fill=False, color='darkblue', 
           linewidth=2, ax=ax)

# Normal distribution overlay
x_range = np.linspace(daily_returns.min(), daily_returns.max(), 1000)
normal = norm.pdf(x_range, loc=mean, scale=stdev)
ax.plot(x_range, normal, color='red', linewidth=3, linestyle='--', 
        alpha=0.8, label='Normal Distribution')

# Add vertical lines for key statistics
ax.axvline(mean, color='green', linestyle='-', linewidth=2, alpha=0.8, label=f'Mean: {mean:.3f}%')
ax.axvline(mean + stdev, color='orange', linestyle=':', linewidth=2, alpha=0.8, label=f'+1σ: {mean+stdev:.3f}%')
ax.axvline(mean - stdev, color='orange', linestyle=':', linewidth=2, alpha=0.8, label=f'-1σ: {mean-stdev:.3f}%')

# Highlight tail areas (beyond 2 standard deviations)
tail_left = mean - 2*stdev
tail_right = mean + 2*stdev
y_max = ax.get_ylim()[1]

# Add shaded regions for extreme events
x_fill_left = x_range[x_range <= tail_left]
x_fill_right = x_range[x_range >= tail_right]
if len(x_fill_left) > 0:
    y_fill_left = norm.pdf(x_fill_left, loc=mean, scale=stdev)
    ax.fill_between(x_fill_left, 0, y_fill_left, alpha=0.3, color='red', label='Extreme Losses')
if len(x_fill_right) > 0:
    y_fill_right = norm.pdf(x_fill_right, loc=mean, scale=stdev)
    ax.fill_between(x_fill_right, 0, y_fill_right, alpha=0.3, color='green', label='Extreme Gains')

# Enhance titles and labels
ax.set_title('Short Strangle Strategy: Daily Returns Distribution Analysis', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Daily P&L (%)', fontsize=12, fontweight='bold')
ax.set_ylabel('Probability Density', fontsize=12, fontweight='bold')

# Add statistics box
stats_text = f"""Statistical Summary:
Mean: {mean:.3f}%
Std Dev: {stdev:.3f}%
Skewness: {skewness:.3f}
Kurtosis: {kurt:.3f}
Jarque-Bera p-value: {jb_pvalue:.4f}
Sample Size: {len(daily_returns)}"""

# Create a text box with statistics
props = dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.8)
ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props, fontfamily='monospace')

# Improve legend
ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True, fontsize=10)

# Add grid customization
ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
ax.set_facecolor('white')

# Improve tick formatting
ax.tick_params(axis='both', which='major', labelsize=10)

# Add interpretation text at the bottom
interpretation = "Red dashed line shows normal distribution assumption vs. actual data (blue). Deviations suggest non-normal returns."
fig.text(0.5, 0.02, interpretation, ha='center', fontsize=10, style='italic', color='gray')

plt.tight_layout()
plt.show()

# Optional: Additional analysis plots
fig2, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

# Q-Q plot for normality assessment
from scipy import stats
stats.probplot(daily_returns, dist="norm", plot=ax1)
ax1.set_title('Q-Q Plot: Normal Distribution Check', fontweight='bold')
ax1.grid(True, alpha=0.3)

# Box plot
ax2.boxplot(daily_returns, vert=True)
ax2.set_title('Box Plot: Outlier Detection', fontweight='bold')
ax2.set_ylabel('Daily P&L (%)')
ax2.grid(True, alpha=0.3)

# Histogram with multiple bins
ax3.hist(daily_returns, bins=30, alpha=0.7, color='steelblue', edgecolor='black')
ax3.axvline(mean, color='red', linestyle='--', linewidth=2)
ax3.set_title('Histogram: Return Distribution', fontweight='bold')
ax3.set_xlabel('Daily P&L (%)')
ax3.set_ylabel('Frequency')
ax3.grid(True, alpha=0.3)

# Cumulative distribution
sorted_returns = np.sort(daily_returns)
cumulative = np.arange(1, len(sorted_returns) + 1) / len(sorted_returns)
ax4.plot(sorted_returns, cumulative, linewidth=2, color='darkblue', label='Empirical CDF')

# Theoretical normal CDF
theoretical_cdf = norm.cdf(sorted_returns, loc=mean, scale=stdev)
ax4.plot(sorted_returns, theoretical_cdf, linewidth=2, color='red', 
         linestyle='--', label='Normal CDF')
ax4.set_title('Cumulative Distribution Comparison', fontweight='bold')
ax4.set_xlabel('Daily P&L (%)')
ax4.set_ylabel('Cumulative Probability')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Risk metrics calculation
print("\n" + "="*50)
print("RISK ANALYSIS SUMMARY")
print("="*50)
print(f"Value at Risk (95%): {np.percentile(daily_returns, 5):.3f}%")
print(f"Conditional VaR (95%): {daily_returns[daily_returns <= np.percentile(daily_returns, 5)].mean():.3f}%")
print(f"Maximum Drawdown: {daily_returns.min():.3f}%")
print(f"Maximum Gain: {daily_returns.max():.3f}%")
print(f"Sharpe Ratio (daily): {mean/stdev:.3f}")
print(f"Probability of Loss: {(daily_returns < 0).sum()/len(daily_returns)*100:.1f}%")
print(f"Win Rate: {(daily_returns > 0).sum()/len(daily_returns)*100:.1f}%")