"""CLI to price European options (with dividend yield) or compute implied vol."""
import argparse
from .black_scholes import bs_price, bs_greeks, implied_vol

def main():
    p = argparse.ArgumentParser(description="Black–Scholes option pricer (educational)")
    p.add_argument("--S", type=float, required=True, help="Spot price")
    p.add_argument("--K", type=float, required=True, help="Strike")
    p.add_argument("--r", type=float, required=True, help="Risk-free rate (annual, cont. comp)")
    p.add_argument("--T", type=float, required=True, help="Time to maturity in years")
    p.add_argument("--type", choices=["call", "put"], default="call", help="Option type")
    p.add_argument("--sigma", type=float, help="Volatility (annualized). Required unless --iv is passed.")
    p.add_argument("--q", type=float, default=0.0, help="Dividend yield q (annual, cont. comp). Default 0.0")
    p.add_argument("--greeks", action="store_true", help="Also print greeks")    
    p.add_argument("--iv", type=float, help="If provided, interpret as market price and solve for implied vol.")
    args = p.parse_args()

    if args.iv is not None:
        sigma = implied_vol(args.iv, args.S, args.K, args.r, args.T, args.type, args.q)
        print(f"Implied vol (sigma): {sigma:.6f}")
        return

    if args.sigma is None:
        p.error("--sigma is required unless you pass --iv to solve for volatility from price.")

    price = bs_price(args.S, args.K, args.r, args.sigma, args.T, args.type, args.q)
    print(f"{args.type.capitalize()} price: {price:.6f}")

    if args.greeks:
        g = bs_greeks(args.S, args.K, args.r, args.sigma, args.T, args.type, args.q)
        for k, v in g.items():
            print(f"{k.capitalize():<6}: {v:.6f}")

if __name__ == "__main__":
    main()
