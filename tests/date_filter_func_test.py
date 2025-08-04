import pandas as pd
my_date_index = pd.to_datetime(['2012-01-04','2012-01-07','2012-01-02', '2012-02-04', '2012-02-08'])
def filter_closest_to_month_start(date_index = my_date_index):
    df = pd.DataFrame({'dates': date_index})
    closest_dates = df.groupby([df['dates'].dt.year, df['dates'].dt.month])['dates'].min()
    print([d.strftime("%Y-%m-%d") for d in closest_dates])
filter_closest_to_month_start()
