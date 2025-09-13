from scipy.stats import norm, probplot
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def plot_KDE(csv_path):

  # Load data
  equity_curve = pd.read_csv(csv_path, index_col=0)
  daily_returns_df = equity_curve[equity_curve['Daily PnL(%)'] != 0]
  daily_returns = daily_returns_df['Daily PnL(%)']

  # Compute statistics
  mean = daily_returns.mean()
  stdev = daily_returns.std()
  skewness = daily_returns.skew()
  kurt = daily_returns.kurt()
  median = daily_returns.median()
  min_val = daily_returns.min()
  max_val = daily_returns.max()
  mode_val = daily_returns.mode()

  # Create figure with two subplots
  fig, (ax_kde, ax_qq) = plt.subplots(
      1, 2, figsize=(16, 8), facecolor='white', gridspec_kw={'width_ratios': [2, 1]}
  )

  # KDE Plot
  sns.kdeplot(
      x=daily_returns.values,
      fill=True,
      color='darkblue',
      lw=3,
      label='Actual Distribution',
      ax=ax_kde
  )

  x_range = np.linspace(daily_returns.min(), daily_returns.max(), 1000)
  normal = norm.pdf(x_range, loc=mean, scale=stdev)

  lower_threshold = mean - 2 * stdev
  upper_threshold = mean + 2 * stdev

  # Mask extremes
  x_lower_extreme = x_range[x_range < lower_threshold]
  x_upper_extreme = x_range[x_range > upper_threshold]

  y_lower_extreme = norm.pdf(x_lower_extreme, loc=mean, scale=stdev)
  y_upper_extreme = norm.pdf(x_upper_extreme, loc=mean, scale=stdev)

  # Stats text box (position dynamically chosen based on y-limits)
  y_max = ax_kde.get_ylim()[1]
  stats_text = f"""Statistical Summary:
{'-'*20}
Mean: {mean:.3f}%
Median: {median:.3f}%
Std Dev: {stdev:.3f}%
Min Val: {min_val:.3f}%
Max Val: {max_val:.3f}%
Skewness: {skewness:.3f}
Kurtosis: {kurt:.3f}
"""
  props = dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.8)
  ax_kde.text(
      x_range.min(), y_max * 0.9, stats_text, fontsize=10,
      verticalalignment='top', bbox=props, fontfamily='monospace'
  )

  # Fill extreme areas
  ax_kde.fill_between(x_lower_extreme, y_lower_extreme, color='red', alpha=0.5,
                      label=f'Extreme Negative ( < mean-2σ): {round(lower_threshold, 4)} %')
  ax_kde.fill_between(x_upper_extreme, y_upper_extreme, color='green', alpha=0.5,
                      label=f'Extreme Positive ( > mean+2σ): {round(upper_threshold, 4)} %')

  # Mean line
  ax_kde.axvline(mean, color='gray', linestyle=':', label=f'Mean - Actual Distribution : {round(mean, 4)}')

  # Normal distribution curve
  ax_kde.plot(x_range, normal, lw=3, linestyle='--', color='r', label='Normal Distribution')

  # Labels, grid, legend
  ax_kde.set_title('Distribution Analysis - Harvesting VRP via Short Strangles', fontweight = 'bold', fontsize = 14)
  ax_kde.set_ylabel('Probability Density')
  ax_kde.set_xlabel('Daily Returns (%)')
  ax_kde.grid(alpha=0.3)
  ax_kde.legend()

  # Q-Q Plot
  """
  plt.subplot(1,2,2)
  probplot(daily_returns.values, dist = 'norm', plot = plt)
  """
  (osm, osr), (slope, intercept, r) = probplot(daily_returns, dist="norm")
  ax_qq.scatter(osm, osr, s=15, alpha=0.6, label="Sample Quantiles")
  ax_qq.plot(osm, slope * osm + intercept, 'r--', lw=2, label="Normal Line")
  ax_qq.set_title("Q-Q Plot", fontweight = 'bold', fontsize = 14)
  ax_qq.set_xlabel("Theoretical Quantiles")
  ax_qq.set_ylabel("Sample Quantiles")
  ax_qq.legend()
  ax_qq.grid(alpha=0.3)
  plt.tight_layout(pad = 2)
  pos1 = ax_kde.get_position()
  right_edge_x = pos1.x1
  separator_x = right_edge_x + 0.005
  fig.add_artist(plt.Line2D([separator_x, separator_x], [0, 1],
                        transform=fig.transFigure,
                        color='gray', linewidth=2))
  plt.show()
  # print(mode_val)  # Uncomment if you want to inspect mode

if __name__ == "__main__":
  plot_KDE('/Users/pustak/Desktop/Volmageddon/Local_Data/Short Strangle Unit Equity Curve Data.csv')


