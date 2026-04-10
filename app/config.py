"""Configuration — symbols, strike range, expiry, refresh rate."""

# Symbols to track
SYMBOLS = ["NIFTY", "BANKNIFTY"]

# Number of strikes above and below ATM to include
STRIKE_RANGE = 10

# Nearest expiry to use (leave empty to auto-detect)
EXPIRY = ""

# Seconds between each data fetch
REFRESH_INTERVAL = 5
