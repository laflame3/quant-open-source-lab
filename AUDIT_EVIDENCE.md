# Audit evidence

Baseline: `397fdbfebd30` (`main`). This branch establishes the first reproducible
engineering baseline; it does not claim investment alpha.

## Reproduce locally

```powershell
uv sync --locked --group dev
uv run ruff check .
uv run pytest -q
uv run quant-lab backtrader --fast 3 --slow 5 --output artifacts/backtrader-smoke
uv run quant-lab vectorbt --fast 3 --slow 5 --output artifacts/vectorbt-smoke
uv run quant-lab compare --fast 3 --slow 5 --output artifacts/compare-smoke
```

The committed CSV is synthetic. Generated metrics describe only this fixture
and must not be interpreted as out-of-sample evidence. The smoke output is
intentionally ignored; regenerate it with the command above.

## Current evidence boundary

- Implemented: strict OHLCV validation, lagged shared signal helper, structured
  Backtrader/vectorbt outputs, machine-readable comparison, deterministic tests,
  and Windows/Linux CI.
- Not implemented: real market data, development/evaluation
  split, cost/parameter sensitivity, benchmark report, release artifacts.

The comparison contract observes the signal at bar close and executes a target
change at the next bar open. Engine proximity is checked with an explicit
tolerance; bit-for-bit equality is not claimed.
