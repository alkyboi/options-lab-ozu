import math
from options_lab.black_scholes import bs_price

def approx(a, b, tol=1e-6):
    return abs(a - b) <= tol

def test_bs_call_atm():
    # Classical parameter set: S=100, K=100, r=5%, sigma=20%, T=1
    # Reference price ~ 10.4506 (from standard tables)
    price = bs_price(100, 100, 0.05, 0.2, 1.0, 'call')
    assert approx(price, 10.4506, 1e-3)

def test_bs_put_atm_putcall_parity():
    # Use put-call parity to derive expected put
    call = bs_price(100, 100, 0.05, 0.2, 1.0, 'call')
    put  = bs_price(100, 100, 0.05, 0.2, 1.0, 'put')
    # C - P = S - K*exp(-rT)
    lhs = call - put
    rhs = 100 - 100 * math.exp(-0.05 * 1.0)
    assert approx(lhs, rhs, 1e-6)
