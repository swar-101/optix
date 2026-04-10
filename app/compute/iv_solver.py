"""Implied Volatility solver using iterative (Newton-Raphson) method."""

import math
import logging

logger = logging.getLogger(__name__)

_MAX_ITER = 100
_TOL = 1e-6


def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _norm_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def _bs_price(S: float, K: float, T: float, r: float, sigma: float, option_type: str) -> float:
    """Black-Scholes price for a European call or put."""
    if T <= 0 or sigma <= 0:
        return max(0.0, S - K) if option_type == "CE" else max(0.0, K - S)
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    if option_type == "CE":
        return S * _norm_cdf(d1) - K * math.exp(-r * T) * _norm_cdf(d2)
    return K * math.exp(-r * T) * _norm_cdf(-d2) - S * _norm_cdf(-d1)


def _vega(S: float, K: float, T: float, r: float, sigma: float) -> float:
    if T <= 0 or sigma <= 0:
        return 0.0
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    return S * _norm_pdf(d1) * math.sqrt(T)


def solve_iv(
    option: dict,
    r: float = 0.065,
    initial_guess: float | None = None,
) -> float:
    """Return implied volatility for *option* using Newton-Raphson.

    *option* must contain: ``symbol``, ``strike``, ``ltp``, ``option_type``,
    ``underlying_price``, and ``time_to_expiry`` (in years).
    Returns 0.0 when the solver cannot converge.
    """
    S = option.get("underlying_price", 0.0)
    K = option.get("strike", 0.0)
    T = option.get("time_to_expiry", 0.0)
    market_price = option.get("ltp", 0.0)
    option_type = option.get("option_type", "CE")

    if S <= 0 or K <= 0 or T <= 0 or market_price <= 0:
        return 0.0

    sigma = initial_guess if initial_guess and initial_guess > 0 else 0.3

    for _ in range(_MAX_ITER):
        price = _bs_price(S, K, T, r, sigma, option_type)
        v = _vega(S, K, T, r, sigma)
        diff = price - market_price
        if abs(diff) < _TOL:
            return round(sigma, 6)
        if v < 1e-10:
            break
        sigma -= diff / v
        if sigma <= 0:
            sigma = 1e-6

    logger.debug(
        "IV solver did not converge for %s %s %s",
        option.get("symbol"),
        K,
        option_type,
    )
    return 0.0
