# Backtrader

Backtrader is an event-driven Python backtesting framework.

## Source Links

- GitHub: https://github.com/mementum/backtrader
- Documentation: https://www.backtrader.com/docu/
- Quickstart: https://www.backtrader.com/docu/quickstart/quickstart/
- Samples: https://github.com/mementum/backtrader/tree/master/samples

## Learning Status

- Installation notes: `install_notes.md`
- Architecture notes: `architecture_notes.md`
- Examples: `examples/`
- Extra notes: `notes/`

## Minimal Demo

The first local demo is a synthetic-data SMA crossover backtest:

```bash
python3 projects/backtrader/examples/sma_crossover_demo.py
```

Optional parameters:

```bash
python3 projects/backtrader/examples/sma_crossover_demo.py \
  --fast 10 \
  --slow 30 \
  --cash 100000 \
  --stake 100 \
  --commission 0.001
```

Expected output includes:

- strategy parameters
- start and end portfolio value
- buy/sell signal logs
- executed order logs
- closed trade PnL
- total return

## Current Learning Notes

- Backtrader uses `Cerebro` as the central engine for data, strategy, broker, analyzer, and observer coordination.
- Strategy code is written in an event-driven style: each new bar calls `next`.
- This style is useful for understanding order-level behavior before moving to production-grade engines such as Lean.
- The first demo is intentionally simple and uses local synthetic OHLCV data, not external market data.

## Initial Questions

- How does Backtrader organize Cerebro, strategies, data feeds, indicators, brokers, and analyzers?
- How suitable is it for CTA-style trend following and futures backtesting?
- What are the common pitfalls around data alignment, commissions, slippage, and plotting?

## Next Questions

- How should futures contract multipliers and margin be modeled in Backtrader?
- What is the cleanest way to add slippage and commission assumptions for CTA research?
- How should data rolls, missing bars, and night sessions be represented?
- How does the same SMA strategy compare when implemented in vectorbt?
