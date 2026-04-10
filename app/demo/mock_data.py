"""Mock option chain generator for demo mode."""

import random
import math
from datetime import date, timedelta


def generate_mock_chain(
    symbols: list[str],
    num_strikes: int = 10,
    expiry_days: int = 7,
) -> list[dict]:
    """Return a flat list of mock option records.

    Each record matches the output schema expected by the compute layer:
    ``symbol``, ``strike``, ``option_type``, ``ltp``, ``oi``,
    ``underlying_price``, ``time_to_expiry``.
    """
    expiry = date.today() + timedelta(days=expiry_days)
    T = expiry_days / 365.0
    records: list[dict] = []

    atm_prices = {"NIFTY": 22500.0, "BANKNIFTY": 48000.0}
    strike_steps = {"NIFTY": 50.0, "BANKNIFTY": 100.0}

    for symbol in symbols:
        spot = atm_prices.get(symbol, 10000.0) * (1 + random.uniform(-0.005, 0.005))
        step = strike_steps.get(symbol, 50.0)
        atm = round(spot / step) * step

        strikes = [atm + step * i for i in range(-num_strikes, num_strikes + 1)]

        for strike in strikes:
            for option_type in ("CE", "PE"):
                moneyness = (spot - strike) if option_type == "CE" else (strike - spot)
                ltp = max(0.05, moneyness * 0.4 + random.uniform(5, 80))
                oi = random.randint(1000, 500_000)
                records.append(
                    {
                        "symbol": symbol,
                        "strike": strike,
                        "option_type": option_type,
                        "ltp": round(ltp, 2),
                        "oi": oi,
                        "underlying_price": round(spot, 2),
                        "time_to_expiry": T,
                    }
                )

    return records
