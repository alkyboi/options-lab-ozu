# options-lab-ozu

Beginner-friendly options pricing lab for your quant Master's prep.  
Includes a minimal Black–Scholes implementation, tests, and a simple CLI.

## Quickstart

```bash
# 1) Create a virtual environment (Windows PowerShell)
python -m venv .venv
. .venv/Scripts/Activate.ps1

# 2) Install deps
pip install -r requirements.txt

# 3) Run tests
pytest -q

# 4) Use the CLI (call price)
python -m options_lab.cli --S 100 --K 100 --r 0.05 --sigma 0.2 --T 1 --type call
```

## Project layout
```
options-lab-ozu/
├─ src/options_lab/         # Library code
│  ├─ __init__.py
│  ├─ black_scholes.py      # pricing + greeks
│  └─ cli.py                # simple command-line interface
├─ tests/                   # unit tests (pytest)
│  └─ test_black_scholes.py
├─ notebooks/               # put your notebooks here (kept out of git via checkpoints ignore)
├─ data/                    # put raw data here (gitignored by default)
├─ .github/workflows/       # CI
│  └─ python-tests.yml
├─ .gitignore
├─ LICENSE
├─ README.md
└─ requirements.txt
```

## What to try next
- Add binomial pricing as a second model and compare to Black–Scholes.
- Add implied volatility solver and sanity tests.
- Publish to GitHub and enable Actions (CI) to run tests on each push.
