from Method1_data import start_date, end_date
import pandas as pd
from fredapi import Fred
api_key = "23dd8644a8456a82f3dc0e07c51e2a9b"
daily_index = pd.date_range(start = start_date, end = end_date, freq = "D")
fred = Fred(api_key = api_key)
def give_USTY3MO():
    try:
        data = fred.get_series("DGS3MO", start_date, end_date)
        df = data.to_frame(name = "Rates")
        df = df.reindex(daily_index)
        df.index.name = 'Date'
        return df

    except ValueError as err:
        print(f"{err}: The code doesn't exist in fred library") 
USTY3MO = give_USTY3MO()
if __name__ == "__main__":
    print(USTY3MO)