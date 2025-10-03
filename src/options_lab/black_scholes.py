"""Minimal Black–Scholes implementation with greeks (no external deps)."""
from math import log, sqrt, exp, erf, pi

def _phi(x: float) -> float:
    """Standard normal CDF using math.erf."""
    return 0.5 * (1.0 + erf(x / sqrt(2.0)))

def _pdf(x: float) -> float:
    """Standard normal PDF."""
    return (1.0 / sqrt(2.0 * pi)) * exp(-0.5 * x * x)

def _d1(S, K, r, sigma, T):
    return (log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * sqrt(T))

def _d2(d1, sigma, T):
    return d1 - sigma * sqrt(T)

def bs_price(S: float, K: float, r: float, sigma: float, T: float, opt_type: str = "call") -> float:
    """Black–Scholes price for European call/put.

    S: spot price
    K: strike
    r: risk-free rate (annual, cont. comp)
    sigma: volatility (annualized)
    T: time to maturity in years
    opt_type: 'call' or 'put'
    """
    d1 = _d1(S, K, r, sigma, T)
    d2 = _d2(d1, sigma, T)
    if opt_type.lower() == "call":
        return S * _phi(d1) - K * exp(-r * T) * _phi(d2)
    elif opt_type.lower() == "put":
        return K * exp(-r * T) * _phi(-d2) - S * _phi(-d1)
    else:
        raise ValueError("opt_type must be 'call' or 'put'")

def bs_greeks(S: float, K: float, r: float, sigma: float, T: float, opt_type: str = "call") -> dict:
    """Returns Delta, Gamma, Vega, Theta, Rho for a European option."""
    d1 = _d1(S, K, r, sigma, T)
    d2 = _d2(d1, sigma, T)
    pdf = _pdf(d1)

    if opt_type.lower() == "call":
        delta = _phi(d1)
        theta = -(S * pdf * sigma) / (2 * sqrt(T)) - r * K * exp(-r * T) * _phi(d2)
        rho   =  K * T * exp(-r * T) * _phi(d2)
    else:
        delta = _phi(d1) - 1
        theta = -(S * pdf * sigma) / (2 * sqrt(T)) + r * K * exp(-r * T) * _phi(-d2)
        rho   = -K * T * exp(-r * T) * _phi(-d2)

    gamma = pdf / (S * sigma * sqrt(T))
    vega  = S * pdf * sqrt(T)

    return {"delta": delta, "gamma": gamma, "vega": vega, "theta": theta, "rho": rho}
