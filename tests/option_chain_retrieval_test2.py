import wrds
import pandas as pd
weekday_dict = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}

target_ticker = 'SPY'
target_date = pd.Timestamp(2011,10,24)
def Rel_Option_Chain(ticker: str , date: pd.Timestamp) -> pd.DataFrame:
    db = wrds.Connection()
    relevant_year = date.year
    print("\n Finding the most feasible option expiration date to short ... ")
    secid_query = f"""
        select secid, cusip, effect_date, issuer, issue
        from optionm.secnmd
        where ticker = '{ticker}'
        order by effect_date desc limit 1
    """
    info = db.raw_sql(secid_query)
    underlying_secid = info['secid'].iloc[0]

    event_date = date + pd.Timedelta(days=45)
    best_exdate_query = f"""
        select exdate from optionm.opprcd{relevant_year} 
        where secid = {underlying_secid} and date = '{date}' 
        order by abs(exdate - date '{event_date}') limit 2
    """
    best_exdate = pd.Timestamp(db.raw_sql(best_exdate_query)['exdate'].iloc[0])
    display_best_date = best_exdate - pd.Timedelta(days = 1) if best_exdate.weekday() == 5 else best_exdate
    print(f"\n The best valid expiration date seems to be {display_best_date.date()}")
    print(f"\n Retrieving the option chain data for {ticker} on {target_date.date()}({weekday_dict[target_date.weekday()]}) with expiration day on {display_best_date.date()}({weekday_dict[display_best_date.weekday()]}) , it may take some seconds .. ")
    required_options_query = f"""
    select secid, date, exdate, 
    case when extract(dow from exdate) = 6 then exdate - interval '1 day' else exdate
    end as last_trade_date,
    cp_flag, strike_price/1000 as strike_price, best_bid, best_offer, volume, impl_volatility, delta, gamma, vega, theta
    from optionm.opprcd{relevant_year}
    where secid = {underlying_secid} and date = '{target_date}' and exdate = '{best_exdate}'
    """
    required_options = db.raw_sql(required_options_query)
    required_options = required_options[required_options['impl_volatility'].notna()]
    
    return required_options


def Rel_Options(ticker = target_ticker, date = target_date) -> pd.DataFrame:
    rel_chain = Rel_Option_Chain(ticker, date)
    current_date = date
    while rel_chain.empty:
        current_date = current_date + pd.Timedelta(days = 1)
        rel_chain = Rel_Option_Chain(ticker, current_date)
    pos_delta_target = 0.25
    neg_delta_target = -0.25
    #index of row with delta value closest to 0.25
    closest_pos_delta_index = (rel_chain['delta'] - pos_delta_target).abs().idxmin()
    #index of row with delta value closest to -0.25
    closest_min_delta_index = (rel_chain['delta'] - neg_delta_target).abs().idxmin()
    rel_options_df = pd.concat([rel_chain.loc[[closest_pos_delta_index]], rel_chain.loc[[closest_min_delta_index]]], ignore_index=True)
    if rel_options_df['last_trade_date'].iloc[0] != rel_options_df['last_trade_date'].iloc[1]:
        raise ValueError('Same expiration date constraint got violated!')
    return rel_options_df

print(Rel_Options())