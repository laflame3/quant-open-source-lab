# Audit evidence

Baseline: `397fdbfebd30` (`main`). This branch establishes the first reproducible
engineering baseline; it does not claim investment alpha.

## Reproduce locally

```powershell
uv sync --locked --group dev
uv run ruff check .
uv run pytest -q
uv run quant-lab --fast 3 --slow 5 --output artifacts/smoke
```

The committed CSV is synthetic. Generated metrics describe only this fixture
and must not be interpreted as out-of-sample evidence. The smoke output is
intentionally ignored; regenerate it with the command above.

## Current evidence boundary

- Implemented: strict OHLCV validation, lagged shared signal helper, structured
  Backtrader output, deterministic tests, Windows/Linux CI.
- Not implemented: vectorbt parity, real market data, development/evaluation
  split, cost/parameter sensitivity, benchmark report, release artifacts.
