"""Time utilities — expiry calculations and trading-day helpers."""

import math
from datetime import date, datetime, time


_MARKET_OPEN = time(9, 15)
_MARKET_CLOSE = time(15, 30)
_TRADING_DAYS_PER_YEAR = 252


def time_to_expiry(expiry: date, now: datetime | None = None) -> float:
    """Return time to expiry in calendar years.

    Uses calendar days divided by 365 for consistency with standard
    Black-Scholes implementations.
    """
    if now is None:
        now = datetime.now()
    delta = datetime.combine(expiry, _MARKET_CLOSE) - now
    seconds = max(delta.total_seconds(), 0.0)
    return seconds / (365 * 24 * 3600)


def is_market_open(now: datetime | None = None) -> bool:
    """Return *True* if *now* falls within NSE market hours (Mon–Fri)."""
    if now is None:
        now = datetime.now()
    if now.weekday() >= 5:  # Saturday or Sunday
        return False
    return _MARKET_OPEN <= now.time() <= _MARKET_CLOSE
