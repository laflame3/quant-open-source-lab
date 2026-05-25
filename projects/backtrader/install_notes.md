# Backtrader Install Notes

## GitHub URL

- https://github.com/mementum/backtrader
- https://www.backtrader.com/docu/installation/

## Environment

- Date: 2026-05-25
- OS: macOS
- Python: 3.11.9
- Backtrader: 1.9.78.123

## Installation Steps

Install only the core package for the first demo:

```bash
python3 -m pip install backtrader
```

No market data API, token, or large dataset is required for the first demo.

## Verification

```bash
python3 -c "import backtrader as bt; print(bt.__version__)"
```

Expected local result:

```text
1.9.78.123
```

## Problems And Fixes

- Plotting is intentionally skipped in the first demo to avoid optional matplotlib backend issues.
- Data is loaded from a small local CSV to avoid network and vendor-data problems.
- The first demo uses stock-like fixed sizing. Futures margin, contract multipliers, roll logic, and night sessions are left for a later CTA-focused demo.
