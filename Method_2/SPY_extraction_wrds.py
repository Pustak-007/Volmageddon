import wrds
import pandas as pd
import numpy as np
db = wrds.Connection()
def give_permno(target_ticker = 'SPY'):
    permno_query = f"""select permno, ticker, comnam, namedt 
    from crsp.dsenames where ticker = '{target_ticker}' order by namedt desc"""
    helper_df = db.raw_sql(permno_query)
    permno = helper_df['permno'].iloc[0]
    return permno
print(give_permno())

