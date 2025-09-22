#Helped by Claude

import pandas as pd
import numpy as np

def create_linearized_pnl(pnl_csv_path, rebalancing_days_csv_path, trading_days_csv_path):
    # Read input data
    df = pd.read_csv(pnl_csv_path)
    rebalancing_days = pd.read_csv(rebalancing_days_csv_path)
    trading_days = pd.read_csv(trading_days_csv_path)
    
    # Convert dates to datetime
    df['Open_Date'] = pd.to_datetime(df['Open_Date'])
    df['Expiration_date'] = pd.to_datetime(df['Expiration_date'])
    rebalancing_days['Dates'] = pd.to_datetime(rebalancing_days['Dates'])
    trading_days['Dates'] = pd.to_datetime(trading_days['Dates'])

    # Calculate number of trading days between open and expiration
    def count_trading_days(row):
        mask = (trading_days['Dates'] >= row['Open_Date']) & (trading_days['Dates'] <= row['Expiration_date'])
        return len(trading_days[mask])
    
    df['Trading_Days_Held'] = df.apply(count_trading_days, axis=1)
    df['Daily_PnL'] = df['Total PnL'] / df['Trading_Days_Held']

    # Create date range and initialize linearized dataframe
    start_date = df['Open_Date'].min()
    end_date = df['Expiration_date'].max()
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')

    linearized_df = pd.DataFrame({
        'date': date_range,
        'position_0_pnl': 0.0,
        'position_1_pnl': 0.0,
        'daily_pnl': 0.0,
        'is_rebalancing_day': False,
        'is_trading_day': False
    })

    # Mark trading and rebalancing days
    linearized_df.loc[linearized_df['date'].isin(trading_days['Dates']), 'is_trading_day'] = True
    linearized_df.loc[linearized_df['date'].isin(rebalancing_days['Dates']), 'is_rebalancing_day'] = True
    
    # Process only trading days
    trading_dates = linearized_df[linearized_df['is_trading_day']]['date']
    
    for date in trading_dates:
        active_positions = df[
            (df['Open_Date'] <= date) & 
            (df['Expiration_date'] >= date)
        ].sort_values('Open_Date', ascending=True).reset_index()
        
        if len(active_positions) > 0:
            current_month = date.month
            current_year = date.year
            
            for _, position in active_positions.iterrows():
                position_month = position['Open_Date'].month
                position_year = position['Open_Date'].year
                
                if (position_year < current_year) or (position_year == current_year and position_month < current_month):
                    linearized_df.loc[linearized_df['date'] == date, 'position_0_pnl'] = position['Daily_PnL']
                else:
                    linearized_df.loc[linearized_df['date'] == date, 'position_1_pnl'] = position['Daily_PnL']
        
        linearized_df.loc[linearized_df['date'] == date, 'daily_pnl'] = (
            linearized_df.loc[linearized_df['date'] == date, 'position_0_pnl'] +
            linearized_df.loc[linearized_df['date'] == date, 'position_1_pnl']
        )

    # Set non-trading days PnL to 0
    linearized_df.loc[~linearized_df['is_trading_day'], ['position_0_pnl', 'position_1_pnl', 'daily_pnl']] = 0.0
    
    linearized_df['cumulative_pnl'] = linearized_df['daily_pnl'].cumsum()
    return linearized_df

if __name__ == "__main__":
    pnl_csv_path = '/Users/pustak/Desktop/Volmageddon/Local_Data/Final_PnL_DataFrame(Method-2).csv'
    rebalancing_days_csv_path = '/Users/pustak/Desktop/Volmageddon/Local_Data/first_trading_day_of_eachMonth.csv'
    trading_days_csv_path = '/Users/pustak/Desktop/Volmageddon/Local_Data/dinstinct_trading_dates.csv'
    pd.set_option('display.min_rows', 200)
    test_df = create_linearized_pnl(pnl_csv_path, rebalancing_days_csv_path, trading_days_csv_path)
    print(test_df)