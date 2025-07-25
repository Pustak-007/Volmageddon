import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import yfinance as yf 
from matplotlib.ticker import FixedFormatter, FixedLocator, NullLocator
start_date = pd.Timestamp(2011,10,4)
end_date = pd.Timestamp(2024,12,31)
daily_index = pd.date_range(start_date, end_date)
SVXY_data = yf.download('SVXY', start=start_date, end=end_date + pd.Timedelta(days = 1))
SVXY_data = SVXY_data.reindex(index = daily_index)
# Visualization
def Create_SVXY_Curve():
    fig, ax = plt.subplots(figsize=(16,8), dpi=100)
    ax.plot(SVXY_data.index, SVXY_data['Close'], label='SVXY', linewidth=1.5, color='blue')
    ax.set_xlabel('Date', fontsize=14)
    ax.set_ylabel('Value', fontsize=14)
    ax.set_yscale('log')

    # Volmageddon annotation (February 5, 2018)
    volmageddon_pointer_date = pd.Timestamp('2018-02-05')
    volmageddon_pointer_price = 140
    ax.annotate('Volmageddon\n(Feb 5, 2018)',
                xy=(volmageddon_pointer_date, volmageddon_pointer_price),
                xytext=(pd.Timestamp('2020-06-01'), 150),
                fontsize=12,
                bbox=dict(boxstyle="round,pad=0.3", facecolor='red', alpha=0.7),
                arrowprops=dict(arrowstyle='->', lw=2, color='red'))

    # COVID unwinding annotation (March 2020)
    covid_pointer_price = 25
    covid_pointer_date = pd.Timestamp(2020,3,22)
    ax.annotate('COVID Unwinding\n(March 2020)',
                xy=(covid_pointer_date, covid_pointer_price),
                xytext=(covid_pointer_date + pd.Timedelta(days = 60), 40),
                fontsize=12,
                bbox=dict(boxstyle="round,pad=0.3", facecolor='orange', alpha=0.7),
                arrowprops=dict(arrowstyle='->', lw=2, color='orange'))

    #China Shock annotation(August 2015)
    devalue_pointer_price = 70
    devalue_pointer_date = pd.Timestamp(2015,8,30)
    ax.annotate('Chinese Yuan\n Devaluation\n(August 2015)',
                xy = (devalue_pointer_date,devalue_pointer_price),
                xytext = (devalue_pointer_date + pd.Timedelta(days = 50), 150),
                fontsize = 12,
                bbox = dict(boxstyle = "round,pad=0.3", facecolor = 'purple', alpha = 0.7),
                arrowprops=dict(arrowstyle = '->', lw = 2, color = 'purple'))

    # Setting tick values manually - because logarithmic scale creates visualization
    # problems, better to standardize this practice -- because out of all the ones I have tried,
    # this is the one which works consistently
    y_ticks = [10, 20, 30, 40, 50, 70, 100, 150, 200]
    ax.yaxis.set_major_locator(FixedLocator(y_ticks))
    ax.yaxis.set_major_formatter(FixedFormatter(y_ticks))
    ax.yaxis.set_minor_locator(NullLocator())

    # X-axis formatting
    ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    # Grid for better readability
    ax.grid(True, alpha=0.3)

    plt.title('SVXY Index (Log Scale)', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.legend(fontsize=12)
    plt.show()
if __name__ == "__main__":
    print(SVXY_data.loc[pd.Timestamp(2024,12,30), ('Close', 'SVXY')])