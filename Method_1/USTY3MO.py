import pandas as pd
from fredapi import Fred
beginning_date = pd.Timestamp(2012,1,2)
#Note that this beginning day is a weekend - our portfolio begins its action from the very next day
# so - in the equity curve I have set this date as the initial date to set something like a reference beginning point
# where the equity is unaffected by the fluctuation of the market and the strategy involved.
ending_date = pd.Timestamp(2023,2,17)
api_key = "23dd8644a8456a82f3dc0e07c51e2a9b"
if __name__ == "__main__":
    pd.set_option('display.min_rows', 600)
daily_index = pd.date_range(start = beginning_date, end = ending_date, freq = "D")
fred = Fred(api_key = api_key)
def give_USTY3MO():
    try:
        data = fred.get_series("DGS3MO", beginning_date, ending_date)
        df = data.to_frame(name = "Rates")
        df = df.reindex(daily_index)
        df.index.name = 'Date'
        return df

    except ValueError as err:
        print(f"{err}: The code doesn't exist in fred library") 
USTY3MO = give_USTY3MO()
USTY3MO['date'] = USTY3MO.index
USTY3MO.reset_index(drop=True, inplace=True)
new_column_name_order = ['date', 'Rates']
USTY3MO = USTY3MO[new_column_name_order]
if __name__ == "__main__":
    press = 0
    if press == 1:
        USTY3MO.to_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/Fred DGS3MO - Risk Free Proxy.csv')
        #When you open the csv file, the vacant values represent np.nan - NaN values I mean to say.
    if press == 2:    
        print(USTY3MO)
        print('-'*30)
        print(USTY3MO['Rates'].mean())