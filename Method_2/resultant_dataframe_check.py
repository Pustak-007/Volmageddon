import pandas as pd 
if __name__ == "__main__":
    pd.set_option('display.max_rows', None)
my_df = pd.read_csv('/Users/pustak/Desktop/Volmageddon/Local_Data/Final_PnL_DataFrame(Method-2).csv')
print(sum(my_df['Total PnL']))
