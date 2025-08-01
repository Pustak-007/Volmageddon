import wrds
import pandas as pd
if __name__ == "__main__":
    pd.set_option('display.min_rows', 2000)

# Connect to WRDS
db = wrds.Connection()

# Define the ticker we are interested in
target_ticker = 'AAPL'

# Query the master file to find the secid
# We get the most recent record just as a best practice
secid_query = f"""
    select secid, ticker, cusip
    from optionm.secnmd
    where ticker = '{target_ticker}'
    order by effect_date desc
    limit 1
"""

aapl_info = db.raw_sql(secid_query)
aapl_secid = aapl_info['secid'][0]

print(f"Found the secid for {target_ticker}: {aapl_secid}")
# Our target date for the option chain
target_date = '2022-01-18'
aapl_secid = 101594 # The secid we found in Step 1

# Construct the query to get the full option chain for that day
# We select key columns that define an option and its price
option_chain_query = f"""
    select
        date,
        exdate,          -- Expiration date of the option
        cp_flag,         -- 'C' for Call, 'P' for Put
        strike_price,    -- The strike price (needs to be divided by 1000)
        best_bid,        -- The highest price a buyer was willing to pay
        best_offer,      -- The lowest price a seller was willing to accept
        volume,          -- Number of contracts traded on this day
        open_interest,   -- Total number of outstanding contracts
        delta,
        impl_volatility 
    from
        optionm.opprcd2022   -- IMPORTANT: Table name matches the year of our target_date
    where
        secid = {aapl_secid}
        and date = '{target_date}'
"""

# Execute the query
print("Querying the database for the option chain... (This might take a moment)")
aapl_chain_df = db.raw_sql(option_chain_query)

# --- Data Cleaning Step ---
# The strike_price is stored as an integer (e.g., 175000 for $175). We must correct it.
aapl_chain_df['strike_price'] = aapl_chain_df['strike_price'] / 1000.0

print("Query successful!")
print("\n--- Apple Option Chain for 2022-01-18 (First 5 Rows) ---")
#print(aapl_chain_df)
print(aapl_chain_df[aapl_chain_df['impl_volatility']!='<NA>'])