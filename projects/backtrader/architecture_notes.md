# Backtrader Architecture Notes

## Core Concepts

- `Cerebro`: the main engine. It wires together data feeds, strategies, broker settings, analyzers, and observers.
- `Data Feed`: the market data input. The first demo uses `bt.feeds.GenericCSVData`.
- `Strategy`: user-defined trading logic. A strategy receives bars one by one and implements lifecycle methods such as `__init__`, `next`, `notify_order`, and `notify_trade`.
- `Indicator`: reusable time-series calculations. The first demo uses `SimpleMovingAverage` and `CrossOver`.
- `Broker`: simulates cash, positions, order execution, and commission.
- `Analyzer` / `Observer`: optional components for performance statistics and runtime observation.

## Data Flow

```text
CSV data
  -> GenericCSVData
  -> Cerebro engine
  -> Strategy.next()
  -> Broker order simulation
  -> order/trade notifications
  -> final portfolio value
```

Backtrader is event-driven: the strategy processes historical bars sequentially. This is slower than a fully vectorized workflow, but it is closer to how live trading engines handle data, orders, and portfolio state.

## Strategy Lifecycle

- `__init__`: define indicators and reusable state.
- `next`: called on each new bar after indicators have enough history.
- `buy` / `sell`: submit orders through the broker simulation.
- `notify_order`: inspect completed, canceled, margin, or rejected orders.
- `notify_trade`: inspect closed trade PnL.

The first demo buys when the fast SMA crosses above the slow SMA, and exits when the fast SMA crosses below the slow SMA.

## Useful For My Background

- CTA trend following: Backtrader's event-driven model maps naturally to moving-average, breakout, trailing-stop, and position-management strategies.
- Futures research: the broker and commission abstractions are useful starting points, but realistic futures work needs later extensions for margin, multipliers, rolls, slippage, and trading sessions.
- ML / factor workflow: Backtrader is less convenient for large vectorized factor sweeps, but useful for turning a signal into an order-level simulation.
- Architecture learning: `Cerebro -> Data Feed -> Strategy -> Broker` is a clean way to understand backtest engine design before studying Lean.
