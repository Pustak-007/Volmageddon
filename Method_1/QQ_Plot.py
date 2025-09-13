from scipy.stats import probplot
from scipy.stats import norm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def give_QQ(csv_path):
    """
    Generate Q-Q plot for normality testing of daily returns data.
    
    Args:
        csv_path (str): Path to CSV file containing equity curve data
        
    Returns:
        Just plots the data and then done - doesn't return anything
    """
    # Load data
    equity_curve = pd.read_csv(csv_path, index_col=0)
    daily_returns_df = equity_curve[equity_curve['Daily PnL(%)'] != 0]
    daily_returns = daily_returns_df['Daily PnL(%)']
    mean = daily_returns.mean()
    stdev = daily_returns.std()
    x_range = np.linspace(daily_returns.min(), daily_returns.max(), 1000)
    normal_sample = np.random.normal(loc = mean, scale = stdev, size = len(daily_returns))

    # Create single subplot for Q-Q plot
    fig, axes = plt.subplots(1, 2, figsize=(16, 8), facecolor='white')
    ax_qq, ax_nqq = axes
    
    # Q-Q Plot
    (osm, osr), (slope, intercept, r) = probplot(daily_returns, dist="norm")
    ax_qq.scatter(osm, osr, s=15, alpha=0.6, label="Sample Quantiles")
    ax_qq.plot(osm, slope * osm + intercept, 'r--', lw=2, label="Normal Line")
    if csv_path == '/Users/pustak/Desktop/Volmageddon/Local_Data/SVXY Unit Equity Curve Data.csv':
        ax_qq.set_title("SVXY Long Strategy Distribution Q-Q Plot", fontweight='bold', fontsize=14)
    if csv_path == '/Users/pustak/Desktop/Volmageddon/Local_Data/SPY Unit Equity Curve Data.csv':
        ax_qq.set_title("SPY Long Strategy (Benchmark) Distribution Q-Q Plot", fontweight = 'bold', fontsize = 14)    
    ax_qq.set_xlabel("Theoretical Quantiles")
    ax_qq.set_ylabel("Sample Quantiles")
    ax_qq.legend()
    ax_qq.grid(alpha=0.3)

    #Normal Q-Q plot
    (osm, osr), (slope, intercept, r) = probplot(normal_sample, dist = "norm")
    ax_nqq.scatter(osm, osr, s=15, alpha=0.6, label="Normal Sample Quantiles")
    ax_nqq.plot(osm, slope * osm + intercept, 'r--', lw=2, label="Normal Line")
    ax_nqq.set_title("Normal Q-Q Plot", fontweight='bold', fontsize=14)
    ax_nqq.set_xlabel("Theoretical Quantiles")
    ax_nqq.set_ylabel("Sample Quantiles")
    ax_nqq.legend()
    ax_nqq.grid(alpha=0.3)

    plt.tight_layout(pad = 2)
    pos1 = ax_qq.get_position()
    right_edge_x = pos1.x1
    separator_x = right_edge_x + 0.005
    fig.add_artist(plt.Line2D([separator_x, separator_x], [0, 1],
                        transform=fig.transFigure,
                        color='gray', linewidth=2))
    plt.show()


if __name__ == "__main__":
    give_QQ('/Users/pustak/Desktop/Volmageddon/Local_Data/SPY Unit Equity Curve Data.csv')
    