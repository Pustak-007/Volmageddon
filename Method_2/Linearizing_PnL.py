import pandas as pd
import numpy as np

def create_linearized_pnl(pnl_csv_path, rebalancing_days_csv_path):
    df = pd.read_csv(pnl_csv_path)
    rebalancing_days = pd.read_csv(rebalancing_days_csv_path)
    
    df['Open_Date'] = pd.to_datetime(df['Open_Date'])
    df['Expiration_date'] = pd.to_datetime(df['Expiration_date'])
    rebalancing_days['Dates'] = pd.to_datetime(rebalancing_days['Dates'])
    
    df['Days_Held'] = (df['Expiration_date'] - df['Open_Date']).dt.days + 1
    df['Daily_PnL'] = df['Total PnL'] / df['Days_Held']

    start_date = df['Open_Date'].min()
    end_date = df['Expiration_date'].max()
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')

    linearized_df = pd.DataFrame({
        'date': date_range,
        'position_0_pnl': 0.0,  # PnL from previous month's position
        'position_1_pnl': 0.0,  # PnL from current month's position
        'daily_pnl': 0.0,
        'is_rebalancing_day': False
    })

    linearized_df.loc[linearized_df['date'].isin(rebalancing_days['Dates']), 'is_rebalancing_day'] = True
    
    for date in date_range:
        active_positions = df[
            (df['Open_Date'] <= date) & 
            (df['Expiration_date'] >= date)
        ].sort_values('Open_Date', ascending=True).reset_index()
        
        if len(active_positions) > 0:
            # Check if this is from current month or previous month
            current_month = date.month
            current_year = date.year
            
            for _, position in active_positions.iterrows():
                position_month = position['Open_Date'].month
                position_year = position['Open_Date'].year
                
                if (position_year < current_year) or (position_year == current_year and position_month < current_month):
                    # This is previous month's position
                    linearized_df.loc[linearized_df['date'] == date, 'position_0_pnl'] = position['Daily_PnL']
                else:
                    # This is current month's position
                    linearized_df.loc[linearized_df['date'] == date, 'position_1_pnl'] = position['Daily_PnL']
        
        linearized_df.loc[linearized_df['date'] == date, 'daily_pnl'] = (
            linearized_df.loc[linearized_df['date'] == date, 'position_0_pnl'] +
            linearized_df.loc[linearized_df['date'] == date, 'position_1_pnl']
        )

    linearized_df['cumulative_pnl'] = linearized_df['daily_pnl'].cumsum()   
    return linearized_df

if __name__ == "__main__":
    pnl_csv_path = '/Users/pustak/Desktop/Volmageddon/Local_Data/Final_PnL_DataFrame(Method-2).csv'
    rebalancing_days_csv_path = '/Users/pustak/Desktop/Volmageddon/Local_Data/first_trading_day_of_eachMonth.csv'
    pd.set_option('display.min_rows', 400)
    print(create_linearized_pnl(pnl_csv_path, rebalancing_days_csv_path))