import math
from options_lab.black_scholes import bs_price, implied_vol

def approx(a, b, tol=1e-4):
    return abs(a - b) <= tol

def test_bs_putcall_parity_with_q():
    S, K, r, sigma, T, q = 100, 100, 0.05, 0.2, 1.0, 0.02
    call = bs_price(S, K, r, sigma, T, 'call', q)
    put  = bs_price(S, K, r, sigma, T, 'put',  q)
    lhs = call - put
    rhs = S * math.exp(-q*T) - K * math.exp(-r*T)
    assert approx(lhs, rhs, 1e-6)

def test_dividend_yield_lowers_call_price():
    S, K, r, sigma, T = 100, 100, 0.05, 0.2, 1.0
    c0 = bs_price(S, K, r, sigma, T, 'call', q=0.0)
    c1 = bs_price(S, K, r, sigma, T, 'call', q=0.03)
    assert c1 < c0  # higher q should lower call value (all else equal)

def test_implied_vol_recovers_true_sigma():
    S, K, r, sigma_true, T, q = 100, 100, 0.05, 0.35, 1.0, 0.01
    market = bs_price(S, K, r, sigma_true, T, 'call', q)
    est = implied_vol(market, S, K, r, T, 'call', q)
    assert approx(est, sigma_true, 5e-4)
