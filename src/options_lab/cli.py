"""Simple CLI to price European options using Black–Scholes."""
import argparse
from .black_scholes import bs_price, bs_greeks

def main():
    p = argparse.ArgumentParser(description="Black–Scholes option pricer (educational)")
    p.add_argument("--S", type=float, required=True, help="Spot price")
    p.add_argument("--K", type=float, required=True, help="Strike")
    p.add_argument("--r", type=float, required=True, help="Risk-free rate (annual)")
    p.add_argument("--sigma", type=float, required=True, help="Volatility (annualized)")
    p.add_argument("--T", type=float, required=True, help="Time to maturity in years")
    p.add_argument("--type", choices=["call", "put"], default="call", help="Option type")
    p.add_argument("--greeks", action="store_true", help="Also print greeks")    
    args = p.parse_args()

    price = bs_price(args.S, args.K, args.r, args.sigma, args.T, args.type)
    print(f"{args.type.capitalize()} price: {price:.6f}")

    if args.greeks:
        g = bs_greeks(args.S, args.K, args.r, args.sigma, args.T, args.type)
        for k, v in g.items():
            print(f"{k.capitalize():<6}: {v:.6f}")

if __name__ == "__main__":
    main()
