"""Callable Backtrader adapter with structured outputs."""

import backtrader as bt
import pandas as pd

from quant_open_source_lab.config import BacktestConfig
from quant_open_source_lab.data import load_ohlcv
from quant_open_source_lab.metrics import performance_metrics
from quant_open_source_lab.schemas import BacktestResult


class SmaCrossoverStrategy(bt.Strategy):
    params = (("fast", 10), ("slow", 30), ("stake", 100))

    def __init__(self) -> None:
        self.pending = None
        self.executions: list[dict[str, object]] = []
        self.equity_rows: list[dict[str, object]] = []
        fast = bt.indicators.SimpleMovingAverage(self.data.close, period=self.p.fast)
        slow = bt.indicators.SimpleMovingAverage(self.data.close, period=self.p.slow)
        self.cross = bt.indicators.CrossOver(fast, slow)

    def notify_order(self, order: bt.Order) -> None:
        if order.status in (order.Submitted, order.Accepted):
            return
        if order.status == order.Completed:
            self.executions.append(
                {
                    "date": self.data.datetime.date(0).isoformat(),
                    "side": "buy" if order.isbuy() else "sell",
                    "price": float(order.executed.price),
                    "size": float(order.executed.size),
                    "commission": float(order.executed.comm),
                }
            )
        self.pending = None

    def next(self) -> None:
        self.equity_rows.append(
            {
                "date": self.data.datetime.date(0).isoformat(),
                "equity": float(self.broker.getvalue()),
                "position": float(self.position.size),
            }
        )
        if self.pending:
            return
        if not self.position and self.cross > 0:
            self.pending = self.buy(size=self.p.stake)
        elif self.position and self.cross < 0:
            self.pending = self.sell(size=self.position.size)

    def stop(self) -> None:
        # Capture final marked-to-market value after the last bar.
        if self.equity_rows:
            self.equity_rows[-1]["equity"] = float(self.broker.getvalue())


def run_backtest(config: BacktestConfig) -> BacktestResult:
    config.validate()
    frame = load_ohlcv(config.data_path)
    feed_frame = frame.copy()
    feed_frame["openinterest"] = 0.0
    cerebro = bt.Cerebro(stdstats=False)
    cerebro.adddata(bt.feeds.PandasData(dataname=feed_frame))
    cerebro.addstrategy(
        SmaCrossoverStrategy, fast=config.fast, slow=config.slow, stake=config.stake
    )
    cerebro.broker.setcash(config.cash)
    cerebro.broker.setcommission(commission=config.commission)
    strategy = cerebro.run()[0]
    equity = pd.DataFrame(strategy.equity_rows)
    trades = pd.DataFrame(
        strategy.executions, columns=["date", "side", "price", "size", "commission"]
    )
    metrics = performance_metrics(equity["equity"])
    metrics.update(
        {
            "trade_count": float(len(trades)),
            "fees": float(trades["commission"].sum()) if not trades.empty else 0.0,
        }
    )
    return BacktestResult("backtrader", metrics, equity, trades)
