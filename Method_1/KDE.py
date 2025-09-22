'''from scipy.stats import norm, gaussian_kde # Import gaussian_kde
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
    
    # This sns.kdeplot is now removed from here to use a more robust method below.
    
    x_range = np.linspace(daily_returns.min(), daily_returns.max(), 1000)
    normal = norm.pdf(x_range, loc=mean, scale=stdev)
    
    lower_threshold = mean - 2 * stdev
    upper_threshold = mean + 2 * stdev
    
    # Mask extremes for the Normal Distribution
    x_lower_extreme = x_range[x_range < lower_threshold]
    x_upper_extreme = x_range[x_range > upper_threshold]
    
    y_lower_extreme = norm.pdf(x_lower_extreme, loc=mean, scale=stdev)
    y_upper_extreme = norm.pdf(x_upper_extreme, loc=mean, scale=stdev)
    
    # Stats text box (position dynamically chosen based on y-limits)
    # We need to plot something first to get the y-limits, so we'll move this down.
    
    # Fill extreme areas for the Normal Distribution (more transparent)
    ax_kde.fill_between(x_lower_extreme, y_lower_extreme, color='red', alpha=0.3,
                       label=f'Normal Extreme Negative (< 2σ)')
    ax_kde.fill_between(x_upper_extreme, y_upper_extreme, color='green', alpha=0.3,
                       label=f'Normal Extreme Positive (> 2σ)')

    # <<< CHANGE START >>>

    # 1. Calculate the KDE data directly using scipy (this is the robust fix)
    kde_actual = gaussian_kde(daily_returns)
    y_kde_actual = kde_actual(x_range)

    # 2. Plot the Actual Distribution using the calculated KDE data
    ax_kde.plot(x_range, y_kde_actual, color='darkblue', lw=3, label='Actual Distribution')
    # Add a fill for the entire actual distribution body
    ax_kde.fill_between(x_range, y_kde_actual, color='darkblue', alpha=0.2)
    
    # 3. Fill the extreme areas for the Actual KDE distribution (less transparent)
    ax_kde.fill_between(x_range, y_kde_actual, where=(x_range < lower_threshold), 
                        color='darkred', alpha=0.6, label='Actual Extreme Negative (< 2σ)')
    ax_kde.fill_between(x_range, y_kde_actual, where=(x_range > upper_threshold), 
                        color='darkgreen', alpha=0.6, label='Actual Extreme Positive (> 2σ)')

    # Theoretical probability from the normal CDF
    prob_normal_outlier = norm.cdf(lower_threshold, loc=mean, scale=stdev)
    # Empirical probability from the actual data
    prob_actual_outlier = (daily_returns < lower_threshold).sum() / len(daily_returns)

    # Now we can safely get the y-limits after plotting
    y_max = ax_kde.get_ylim()[1]
    ax_kde.set_ylim(bottom=0)
    # Stats text box (position dynamically chosen based on y-limits)
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
        x_range.min(), y_max * 0.95, stats_text, fontsize=10,
        va='top', bbox=props, fontfamily='monospace'
    )

    # 5. Create the text box for probabilities
    prob_text = f"""Negative Tail (< {lower_threshold:.2f}%) Probability:
{'-'*40}
Normal Model Prediction: {prob_normal_outlier:.2%}
Actual Occurrences:      {prob_actual_outlier:.2%}
"""
    props_prob = dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.8)
    ax_kde.text(
        -70, 0.025, prob_text, fontsize=10,
        va='center', ha='center', 
        bbox=props_prob, fontfamily='monospace'
    )
    # <<< CHANGE END >>>
    
    # Mean line
    ax_kde.axvline(mean, color='gray', linestyle=':', label=f'Mean: {round(mean, 4)}%')
    
    # Normal distribution curve
    ax_kde.plot(x_range, normal, lw=3, linestyle='--', color='r', label='Normal Distribution')
    
    # Labels, grid, legend
    if 'SVXY' in csv_path:
        ax_kde.set_title('Distribution Analysis - Harvesting VRP via Long SVXY', fontweight = 'bold', fontsize = 14)
    elif 'SPY' in csv_path:
        ax_kde.set_title('Distribution Analysis - Long SPY - Benchmark Strategy')
    ax_kde.set_ylabel('Probability Density')
    ax_kde.set_xlabel('Daily Returns (%)')
    ax_kde.grid(alpha=0.3)
    ax_kde.legend()
    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    give_KDE('/Users/pustak/Desktop/Volmageddon/Local_Data/SVXY Unit Equity Curve Data.csv')
    '''
from scipy.stats import norm, gaussian_kde
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
    
    x_range = np.linspace(daily_returns.min(), daily_returns.max(), 1000)
    normal = norm.pdf(x_range, loc=mean, scale=stdev)
    
    lower_threshold = mean - 2 * stdev
    upper_threshold = mean + 2 * stdev
    
    # Mask extremes for the Normal Distribution
    x_lower_extreme = x_range[x_range < lower_threshold]
    x_upper_extreme = x_range[x_range > upper_threshold]
    
    y_lower_extreme = norm.pdf(x_lower_extreme, loc=mean, scale=stdev)
    y_upper_extreme = norm.pdf(x_upper_extreme, loc=mean, scale=stdev)
    
    # Fill extreme areas for the Normal Distribution (more transparent)
    ax_kde.fill_between(x_lower_extreme, y_lower_extreme, color='red', alpha=0.3,
                       label=f'Normal Extreme Negative (< 2σ)')
    ax_kde.fill_between(x_upper_extreme, y_upper_extreme, color='green', alpha=0.3,
                       label=f'Normal Extreme Positive (> 2σ)')

    # Calculate the KDE data directly using scipy
    kde_actual = gaussian_kde(daily_returns)
    y_kde_actual = kde_actual(x_range)

    # Plot the Actual Distribution using the calculated KDE data
    ax_kde.plot(x_range, y_kde_actual, color='darkblue', lw=3, label='Actual Distribution')
    ax_kde.fill_between(x_range, y_kde_actual, color='darkblue', alpha=0.2)
    
    # Fill the extreme areas for the Actual KDE distribution
    ax_kde.fill_between(x_range, y_kde_actual, where=(x_range < lower_threshold), 
                        color='darkred', alpha=0.6, label='Actual Extreme Negative (< 2σ)')
    ax_kde.fill_between(x_range, y_kde_actual, where=(x_range > upper_threshold), 
                        color='darkgreen', alpha=0.6, label='Actual Extreme Positive (> 2σ)')

    y_max = ax_kde.get_ylim()[1]
    
    # Stats text box
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
        x_range.min(), y_max * 0.95, stats_text, fontsize=10,
        va='top', bbox=props, fontfamily='monospace'
    )
    
    # Negative Tail (< mean - 2*stdev)
    prob_normal_negative = norm.cdf(lower_threshold, loc=mean, scale=stdev)
    prob_actual_negative = (daily_returns < lower_threshold).sum() / len(daily_returns)

    # Positive Tail (> mean + 2*stdev)
    # For a CDF, P(X > a) = 1 - P(X <= a)
    prob_normal_positive = 1 - norm.cdf(upper_threshold, loc=mean, scale=stdev)
    prob_actual_positive = (daily_returns > upper_threshold).sum() / len(daily_returns)

    # Total Outlier Probability (sum of both tails)
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
            va='center', ha = 'center', 
            bbox=props_prob, fontfamily='monospace'
        )
    if "SPY" in csv_path:
        props_prob = dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.8)
        ax_kde.text(
            x_range.min(), 0.3, prob_text, fontsize=10,
            va='top', 
            bbox=props_prob, fontfamily='monospace'
        )          

    ax_kde.axvline(mean, color='gray', linestyle=':', label=f'Mean: {round(mean, 4)}%')
    
    # Normal distribution curve
    ax_kde.plot(x_range, normal, lw=3, linestyle='--', color='r', label='Normal Distribution')
    
    # Labels, grid, legend
    if 'SVXY' in csv_path:
        ax_kde.set_title('KDE Plot - Daily Returns of Harvesting VRP via Long SVXY', fontweight = 'bold', fontsize = 14)
    elif 'SPY' in csv_path:
        ax_kde.set_title('KDE Plot - Daily Returns of SPY Long & Hold (Benchmark Strategy)', fontweight = 'bold', fontsize = 14)
    ax_kde.set_ylabel('Probability Density', fontsize = 12, fontweight = 'bold')
    ax_kde.set_xlabel('Daily Returns (%)', fontsize = 12, fontweight = 'bold')
    ax_kde.grid(alpha=0.3)
    
    # Force the y-axis to start at 0
    ax_kde.set_ylim(bottom=0)
    
    ax_kde.legend()
    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    give_KDE('/Users/pustak/Desktop/Volmageddon/Local_Data/SPY Unit Equity Curve Data.csv')