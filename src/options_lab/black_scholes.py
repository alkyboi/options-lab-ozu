"""Black–Scholes with continuous dividend yield `q` + Greeks + implied volatility.

All rates are annualized and continuously compounded.
"""
from math import log, sqrt, exp, erf, pi, isfinite

def _phi(x: float) -> float:
    """Standard normal CDF using math.erf."""
    return 0.5 * (1.0 + erf(x / sqrt(2.0)))

def _pdf(x: float) -> float:
    """Standard normal PDF."""
    return (1.0 / sqrt(2.0 * pi)) * exp(-0.5 * x * x)

def _d1(S, K, r, sigma, T, q):
    return (log(S / K) + (r - q + 0.5 * sigma * sigma) * T) / (sigma * sqrt(T))

def _d2(d1, sigma, T):
    return d1 - sigma * sqrt(T)

def bs_price(S: float, K: float, r: float, sigma: float, T: float, opt_type: str = "call", q: float = 0.0) -> float:
    """Black–Scholes price for a European call/put with dividend yield q.

    S: spot price
    K: strike
    r: risk-free rate (annual, cont. comp)
    sigma: volatility (annualized)
    T: time to maturity in years
    opt_type: 'call' or 'put'
    q: continuous dividend yield (annual, cont. comp). For non-dividend underlyings use 0.
    """
    if sigma <= 0 or T <= 0 or S <= 0 or K <= 0:
        raise ValueError("Inputs must be positive and sigma,T>0")
    d1 = _d1(S, K, r, sigma, T, q)
    d2 = _d2(d1, sigma, T)
    df_r = exp(-r * T)
    df_q = exp(-q * T)

    if opt_type.lower() == "call":
        return S * df_q * _phi(d1) - K * df_r * _phi(d2)
    elif opt_type.lower() == "put":
        return K * df_r * _phi(-d2) - S * df_q * _phi(-d1)
    else:
        raise ValueError("opt_type must be 'call' or 'put'")

def bs_greeks(S: float, K: float, r: float, sigma: float, T: float, opt_type: str = "call", q: float = 0.0) -> dict:
    """Returns Delta, Gamma, Vega, Theta, Rho for a European option with dividend yield q.
    Theta is per-year; Vega and Rho are per 1.00 change in sigma/r (per vol-point ~ vega*0.01).
    """
    d1 = _d1(S, K, r, sigma, T, q)
    d2 = _d2(d1, sigma, T)
    pdf = _pdf(d1)
    df_r = exp(-r * T)
    df_q = exp(-q * T)

    if opt_type.lower() == "call":
        delta = df_q * _phi(d1)
        theta = -(S * df_q * pdf * sigma) / (2 * sqrt(T)) - r * K * df_r * _phi(d2) + q * S * df_q * _phi(d1)
        rho   =  K * T * df_r * _phi(d2)
    else:
        delta = df_q * (_phi(d1) - 1)
        theta = -(S * df_q * pdf * sigma) / (2 * sqrt(T)) + r * K * df_r * _phi(-d2) - q * S * df_q * _phi(-d1)
        rho   = -K * T * df_r * _phi(-d2)

    gamma = df_q * pdf / (S * sigma * sqrt(T))
    vega  = S * df_q * pdf * sqrt(T)

    return {"delta": delta, "gamma": gamma, "vega": vega, "theta": theta, "rho": rho}

def implied_vol(target_price: float, S: float, K: float, r: float, T: float, opt_type: str = "call", q: float = 0.0,
                tol: float = 1e-8, max_iter: int = 100, lo: float = 1e-6, hi: float = 5.0) -> float:
    """Solve for Black–Scholes implied volatility using a robust bisection method.

    target_price: market price of the option
    returns: sigma (vol) such that bs_price(..., sigma, ...) ~= target_price
    """
    if target_price <= 0:
        raise ValueError("target_price must be positive")

    # Bisection bracket: ensure monotonicity by checking prices at bounds
    def price(sig):
        return bs_price(S, K, r, sig, T, opt_type, q)

    lo_p = price(lo)
    hi_p = price(hi)
    # If the target is outside bounds, expand once
    if target_price < lo_p:
        return lo  # close to zero vol; better than failing
    if target_price > hi_p:
        # try expanding hi to 10.0
        hi2 = 10.0
        if price(hi2) < target_price:
            return hi2  # extremely high vol scenario
        hi, hi_p = hi2, price(hi2)

    a, b = lo, hi
    fa = price(a) - target_price
    fb = price(b) - target_price

    for _ in range(max_iter):
        m = 0.5 * (a + b)
        fm = price(m) - target_price
        if abs(fm) < tol:
            return m
        # choose the side that brackets the root
        if fa * fm <= 0:
            b, fb = m, fm
        else:
            a, fa = m, fm

    return 0.5 * (a + b)  # best effort
