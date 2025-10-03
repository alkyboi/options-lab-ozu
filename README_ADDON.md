## New features
- **Dividend yield `q`** supported in pricing and Greeks.
- **Implied volatility solver** via robust bisection.

### CLI examples
```bash
# Price with dividend yield
python -m options_lab.cli --S 100 --K 100 --r 0.05 --sigma 0.2 --T 1 --type call --q 0.02 --greeks

# Solve implied vol from a market price (pass --iv instead of --sigma)
python -m options_lab.cli --S 100 --K 100 --r 0.05 --T 1 --type call --q 0.02 --iv 9.85
```
