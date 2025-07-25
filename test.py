from ib_insync import *

# Initialize the IB client
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=12)

# Define the underlying contract (NVIDIA stock)
underlying = Stock('NVDA', 'SMART', 'USD')
ib.qualifyContracts(underlying)  # Ensures the contract is fully specified

# Request option chain parameters
option_chains = ib.reqSecDefOptParams(
    underlying.symbol, '', underlying.secType, underlying.conId
)

# Process the results
for chain in option_chains:
    print(f"Exchange: {chain.exchange}")
    print(f"Underlying ConId: {chain.underlyingConId}")
    print(f"Trading Class: {chain.tradingClass}")
    print(f"Multiplier: {chain.multiplier}")
    print(f"Expirations: {chain.expirations}")
    print(f"Strikes: {chain.strikes}")
    print('-' * 50)

ib.disconnect()