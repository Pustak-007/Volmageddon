#The code and most of the functions will be similar to the KPIs.py file in Method_1
#The regimes we are analyzing have to be the same as the ones as Longing SVXY Method - for the sake of consistency.

import pandas as pd
def number_of_years(end_date, begin_date):
    b_date = pd.to_datetime(begin_date)
    e_date = pd.to_datetime(end_date)
    if e_date < b_date:
        raise ValueError ("Make sure you enter end_date first and begin_date second.")
    return ((e_date-b_date).days)/365.25

period_list = {'All' : (pd.Timestamp(2011,10,4), pd.Timestamp(2024,12,31)),
               'Golden Era' : (pd.Timestamp(2011,10,5), pd.Timestamp(2018,1,31)),
               'Volmageddon' : (pd.Timestamp(2018,2,1),pd.Timestamp(2018,2,28)),
               'Post-Volmageddon/Pre-COVID' : (pd.Timestamp(2018,3,1), pd.Timestamp(2020,1,31)),
               'COVID-19':(pd.Timestamp(2020,2,1), pd.Timestamp(2020,4,30)),
               'Post-COVID': (pd.Timestamp(2020,5,1), pd.Timestamp(2024,12,31))}
