# Daily Learning Log

## 2026-05-25

### Focus

- Initialize the quant open-source learning lab.
- Read Backtrader README/docs structure and implement the first minimal SMA crossover demo.

### What I Read

- Backtrader GitHub repository: https://github.com/mementum/backtrader
- Backtrader quickstart documentation: https://www.backtrader.com/docu/quickstart/quickstart/
- Backtrader samples directory: https://github.com/mementum/backtrader/tree/master/samples
- Backtrader core package structure, including `cerebro`, `strategy`, `feeds`, `indicators`, `broker`, `analyzers`, and `observers`.

### What I Ran

- `python3 -c "import backtrader as bt; print(bt.__version__)"`
- `python3 projects/backtrader/examples/sma_crossover_demo.py`

### What I Learned

- Backtrader is centered on the `Cerebro` engine.
- Strategy logic is event-driven and runs bar by bar through `next`.
- `notify_order` and `notify_trade` are important for understanding execution and PnL.
- A minimal local CSV demo is enough to understand the basic engine flow without external data dependencies.

### Problems

- Plotting is skipped for now to avoid optional matplotlib backend issues.
- The first demo is not yet a realistic futures backtest because it does not model margin, contract multipliers, rolls, or night sessions.

### Next Step

- Extend Backtrader notes with futures-specific commission, slippage, and contract settings.
- Implement the same SMA logic in vectorbt later for event-driven vs vectorized comparison.
