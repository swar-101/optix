"""Greeks computation (Delta, Gamma, Vega, Theta)."""

import math


def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _norm_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def compute_greeks(
    option: dict,
    iv: float,
    r: float = 0.065,
) -> dict:
    """Return a dict with ``delta``, ``gamma``, ``vega``, and ``theta``.

    Expects *option* to contain ``underlying_price``, ``strike``,
    ``time_to_expiry``, and ``option_type``.
    """
    S = option.get("underlying_price", 0.0)
    K = option.get("strike", 0.0)
    T = option.get("time_to_expiry", 0.0)
    option_type = option.get("option_type", "CE")

    empty = {"delta": 0.0, "gamma": 0.0, "vega": 0.0, "theta": 0.0}

    if S <= 0 or K <= 0 or T <= 0 or iv <= 0:
        return empty

    sqrt_T = math.sqrt(T)
    d1 = (math.log(S / K) + (r + 0.5 * iv ** 2) * T) / (iv * sqrt_T)
    d2 = d1 - iv * sqrt_T
    pdf_d1 = _norm_pdf(d1)
    exp_rT = math.exp(-r * T)

    gamma = pdf_d1 / (S * iv * sqrt_T)
    vega = round(S * pdf_d1 * sqrt_T / 100, 6)  # per 1 % IV move

    if option_type == "CE":
        delta = _norm_cdf(d1)
        theta = (
            -(S * pdf_d1 * iv) / (2 * sqrt_T) - r * K * exp_rT * _norm_cdf(d2)
        ) / 365
    else:
        delta = _norm_cdf(d1) - 1
        theta = (
            -(S * pdf_d1 * iv) / (2 * sqrt_T) + r * K * exp_rT * _norm_cdf(-d2)
        ) / 365

    return {
        "delta": round(delta, 6),
        "gamma": round(gamma, 6),
        "vega": round(vega, 6),
        "theta": round(theta, 6),
    }
