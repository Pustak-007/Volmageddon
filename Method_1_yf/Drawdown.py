import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from Method1_data import SVXY_data
from SPY_data import SPY_data
from matplotlib.ticker import PercentFormatter
from functools import partial
if __name__ == "__main__":
  pd.set_option('display.min_rows', 200)

#This function gives us the different values of drawdowns for different day
def Calculate_Drawdown(data):
    drawdown_data = pd.DataFrame()
    drawdown_data.index = data['Close'].index
    running_max = data['Close'].cummax()
    drawdowns = (data['Close'] - running_max)/running_max * 100 
    drawdown_data['Drawdown (%)'] = drawdowns
    return drawdown_data

#This function gives us the maximum drawdown in particular
def Calculate_Max_Drawdown_Pct(data):
    return Calculate_Drawdown(data)['Drawdown (%)'].min()

SVXY_Drawdown_Data = Calculate_Drawdown(data = SVXY_data.ffill())
SPY_Drawdown_Data = Calculate_Drawdown(data = SPY_data.ffill())

#Plotting
def Plot_Drawdown(data):
    drawdown_data = Calculate_Drawdown(data.ffill())
    x = drawdown_data.index 
    y = drawdown_data['Drawdown (%)']
    fig, ax = plt.subplots(figsize = (16,8), dpi = 100)
    plt.plot(x,y, linewidth = 1.3, color = 'red', label = 'Drawdown Chart')
    #breakeven line
    ax.axhline(y = 0, color = 'gray', linestyle = ':')
    if data.equals(SVXY_data):
      plt.title('Drawdown (%) of Harvesting VRP Strategy via longing SVXY (Linear Scale)', fontsize = 16, fontweight = 'bold')
    else:
      plt.title('Drawdown (%) of SPY - Broader Market (Linear Scale) ', fontsize = 16, fontweight = 'bold')
    plt.xlabel('Date', fontsize = 14)
    plt.ylabel('Drawdown(%)', fontsize = 14)
    plt.grid(True, alpha = 0.3)
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval = 2))
    plt.legend()
    ax.yaxis.set_major_formatter(PercentFormatter(xmax = 100, decimals=2))
    plt.show()
def Plot_Drawdown_SVXY_vs_SPY():
    drawdown_data_SVXY = Calculate_Drawdown(data = SVXY_data.ffill())
    drawdown_data_SPY = Calculate_Drawdown(data = SPY_data.ffill())
    fig, ax = plt.subplots(figsize = (16,8), dpi = 100)
    ax.plot(drawdown_data_SVXY.index,drawdown_data_SVXY['Drawdown (%)'], linewidth = 1.3, color = 'red', label = 'Drawdown Chart SVXY')
    ax.plot(drawdown_data_SPY.index, drawdown_data_SPY['Drawdown (%)'], linewidth = 1.3, color = 'blue', label = 'Drawdown Chart SPY' )
    #breakeven line
    ax.axhline(y = 0, color = 'gray', linestyle = ':')
    ax.set_title('Drawdown (%) of VRP Harvesting via SVXY vs Longing SPY - Broader Market (Linear Scale)', fontsize = 16, fontweight = 'bold')
    ax.set_xlabel('Date', fontsize = 14)
    ax.set_ylabel('Drawdown(%)', fontsize = 14)
    ax.grid(True, alpha = 0.3)
    ax.legend()
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval = 2))
    ax.yaxis.set_major_formatter(PercentFormatter(xmax = 100, decimals=2))
    plt.show()
   
Plot_SVXY_Drawdown = partial(Plot_Drawdown, data = SVXY_data)
Plot_SPY_Drawdown = partial(Plot_Drawdown, data = SPY_data)
if __name__ == "__main__":
   Plot_SVXY_Drawdown()