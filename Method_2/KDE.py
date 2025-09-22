'''
from scipy.stats import norm
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def give_KDE(csv_path):
    """
    Generate KDE plot with statistical analysis for daily returns data.
    
    Args:
        csv_path (str): Path to CSV file containing equity curve data
        
    Returns:
        Just Plots the data - doesn't return anything
    """
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
    
    # Create single subplot for KDE
    fig, ax_kde = plt.subplots(1, 1, figsize=(16, 8), facecolor='white')
    
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
    ax_kde.set_title('Distribution Analysis - Harvesting VRP via Short Strangles', fontweight='bold', fontsize=14)
    ax_kde.set_ylabel('Probability Density')
    ax_kde.set_xlabel('Daily Returns (%)')
    ax_kde.grid(alpha=0.3)
    ax_kde.legend()
    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    give_KDE('/Users/pustak/Desktop/Volmageddon/Local_Data/Short Strangle Unit Equity Curve Data.csv')

'''

from scipy.stats import norm, gaussian_kde
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def give_KDE(csv_path):
    equity_curve = pd.read_csv(csv_path, index_col=0)
    daily_returns_df = equity_curve[equity_curve['Daily PnL(%)'] != 0]
    daily_returns = daily_returns_df['Daily PnL(%)']
    
    mean = daily_returns.mean()
    stdev = daily_returns.std()
    skewness = daily_returns.skew()
    kurt = daily_returns.kurt()
    median = daily_returns.median()
    min_val = daily_returns.min()
    max_val = daily_returns.max()
    mode_val = daily_returns.mode()
    
    # Create single subplot for KDE
    fig, ax_kde = plt.subplots(1, 1, figsize=(16, 8), facecolor='white')
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
    
    # Mask extremes for the Normal Distribution
    x_lower_extreme = x_range[x_range < lower_threshold]
    x_upper_extreme = x_range[x_range > upper_threshold]
    
    y_lower_extreme = norm.pdf(x_lower_extreme, loc=mean, scale=stdev)
    y_upper_extreme = norm.pdf(x_upper_extreme, loc=mean, scale=stdev)
    ax_kde.fill_between(x_lower_extreme, y_lower_extreme, color='red', alpha=0.4,
                       label=f'Normal Extreme Negative (< -2σ)')
    ax_kde.fill_between(x_upper_extreme, y_upper_extreme, color='green', alpha=0.4,
                       label=f'Normal Extreme Positive (> +2σ)')

    kde_actual = gaussian_kde(daily_returns)
    y_kde_actual = kde_actual(x_range)
    ax_kde.fill_between(x_range, y_kde_actual, where=(x_range < lower_threshold), 
                        color='darkred', alpha=1, label='Actual Extreme Negative (< -2σ)')
    ax_kde.fill_between(x_range, y_kde_actual, where=(x_range > upper_threshold), 
                        color='darkgreen', alpha=1, label='Actual Extreme Positive (> +2σ)')

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
    
    prob_normal_negative = norm.cdf(lower_threshold, loc=mean, scale=stdev)
    prob_actual_negative = (daily_returns < lower_threshold).sum() / len(daily_returns)

    prob_normal_positive = 1 - norm.cdf(upper_threshold, loc=mean, scale=stdev)
    prob_actual_positive = (daily_returns > upper_threshold).sum() / len(daily_returns)

    prob_normal_total = prob_normal_negative + prob_normal_positive
    prob_actual_total = prob_actual_negative + prob_actual_positive

    prob_text = f"""Tail Probability Analysis (Beyond 2σ)
{'-'*40}
                  {'Actual':>10s} {'Normal':>10s}
{'Total Outlier:':<15} {prob_actual_total:>9.2%} {prob_normal_total:>10.2%}
{'Negative Tail:':<15} {prob_actual_negative:>9.2%} {prob_normal_negative:>10.2%}
{'Positive Tail:':<15} {prob_actual_positive:>9.2%} {prob_normal_positive:>10.2%}
"""
    
    if "SVXY" in csv_path:
        props_prob = dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.8)
        ax_kde.text(
            -70, 0.09, prob_text, fontsize=10,
            va='center', ha='center', 
            bbox=props_prob, fontfamily='monospace'
        )
    elif "SPY" in csv_path:
        props_prob = dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.8)
        ax_kde.text(
            x_range.min(), 0.3, prob_text, fontsize=10,
            va='top', 
            bbox=props_prob, fontfamily='monospace'
        )
    else:
        props_prob = dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.8)
        ax_kde.text(
            x_range.min(), 0.4, prob_text, fontsize=10,
            va='center', 
            bbox=props_prob, fontfamily='monospace'
        )

    ax_kde.axvline(mean, color='gray', linestyle=':', label=f'Mean - Actual Distribution : {round(mean, 4)}%')
    
    ax_kde.plot(x_range, normal, lw=3, linestyle='--', color='r', label='Normal Distribution')
    
    if 'SVXY' in csv_path:
        ax_kde.set_title('KDE Plot - Daily Returns of Harvesting VRP via Long SVXY', fontweight='bold', fontsize=14)
    elif 'SPY' in csv_path:
        ax_kde.set_title('KDE Plot - Daily Returns of SPY Long & Hold (Benchmark Strategy)', fontweight='bold', fontsize=14)
    elif 'Short Strangle' in csv_path:
        ax_kde.set_title('KDE Plot - Daily Returns of Harvesting VRP via SPY Short Strangles', fontweight='bold', fontsize=14)
    else:
        ax_kde.set_title('KDE Plot - Daily Returns Distributional Analysis', fontweight='bold', fontsize=14)
    
    ax_kde.set_ylabel('Probability Density', fontsize = 12, fontweight = 'bold')
    ax_kde.set_xlabel('Daily Returns (%)', fontsize = 12, fontweight = 'bold')
    ax_kde.grid(alpha=0.3)
    
    ax_kde.set_ylim(bottom=0)
    
    ax_kde.legend()
    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    give_KDE('/Users/pustak/Desktop/Volmageddon/Local_Data/Short Strangle Unit Equity Curve Data.csv')


