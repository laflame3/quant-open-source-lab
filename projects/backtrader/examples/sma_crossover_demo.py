#!/usr/bin/env python3
"""Minimal Backtrader SMA crossover demo.

Run from the repository root:
    python3 projects/backtrader/examples/sma_crossover_demo.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

import backtrader as bt


DEFAULT_DATA_PATH = Path(__file__).with_name("data") / "synthetic_ohlcv.csv"


class SmaCrossoverStrategy(bt.Strategy):
    """Buy on fast SMA crossing above slow SMA, sell on the reverse cross."""

    params = (
        ("fast", 10),
        ("slow", 30),
        ("stake", 100),
    )

    def __init__(self) -> None:
        self.order = None
        self.fast_sma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.p.fast
        )
        self.slow_sma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.p.slow
        )
        self.crossover = bt.indicators.CrossOver(self.fast_sma, self.slow_sma)

    def log(self, message: str) -> None:
        dt = self.datas[0].datetime.date(0).isoformat()
        print(f"{dt} | {message}")

    def notify_order(self, order: bt.Order) -> None:
        if order.status in (order.Submitted, order.Accepted):
            return

        if order.status == order.Completed:
            action = "BUY" if order.isbuy() else "SELL"
            self.log(
                f"{action} EXECUTED | price={order.executed.price:.2f}, "
                f"size={order.executed.size:.0f}, "
                f"value={order.executed.value:.2f}, "
                f"commission={order.executed.comm:.2f}"
            )
        elif order.status in (order.Canceled, order.Margin, order.Rejected):
            self.log(f"ORDER FAILED | status={order.getstatusname()}")

        self.order = None

    def notify_trade(self, trade: bt.Trade) -> None:
        if trade.isclosed:
            self.log(
                f"TRADE CLOSED | gross_pnl={trade.pnl:.2f}, "
                f"net_pnl={trade.pnlcomm:.2f}"
            )

    def next(self) -> None:
        if self.order:
            return

        if not self.position and self.crossover > 0:
            self.log(
                f"BUY SIGNAL | close={self.data.close[0]:.2f}, "
                f"fast_sma={self.fast_sma[0]:.2f}, "
                f"slow_sma={self.slow_sma[0]:.2f}"
            )
            self.order = self.buy(size=self.p.stake)
        elif self.position and self.crossover < 0:
            self.log(
                f"SELL SIGNAL | close={self.data.close[0]:.2f}, "
                f"fast_sma={self.fast_sma[0]:.2f}, "
                f"slow_sma={self.slow_sma[0]:.2f}"
            )
            self.order = self.sell(size=self.position.size)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a minimal Backtrader SMA crossover demo."
    )
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA_PATH)
    parser.add_argument("--fast", type=int, default=10)
    parser.add_argument("--slow", type=int, default=30)
    parser.add_argument("--cash", type=float, default=100000.0)
    parser.add_argument("--stake", type=int, default=100)
    parser.add_argument("--commission", type=float, default=0.001)
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    if args.fast <= 0 or args.slow <= 0:
        raise ValueError("SMA windows must be positive integers.")
    if args.fast >= args.slow:
        raise ValueError("--fast must be smaller than --slow for this demo.")
    if args.cash <= 0:
        raise ValueError("--cash must be positive.")
    if args.stake <= 0:
        raise ValueError("--stake must be positive.")
    if args.commission < 0:
        raise ValueError("--commission cannot be negative.")
    if not args.data.exists():
        raise FileNotFoundError(f"Data file not found: {args.data}")


def build_data_feed(data_path: Path) -> bt.feeds.GenericCSVData:
    return bt.feeds.GenericCSVData(
        dataname=str(data_path),
        dtformat="%Y-%m-%d",
        datetime=0,
        open=1,
        high=2,
        low=3,
        close=4,
        volume=5,
        openinterest=-1,
        headers=True,
    )


def run_backtest(args: argparse.Namespace) -> None:
    cerebro = bt.Cerebro()
    cerebro.adddata(build_data_feed(args.data))
    cerebro.addstrategy(
        SmaCrossoverStrategy,
        fast=args.fast,
        slow=args.slow,
        stake=args.stake,
    )
    cerebro.broker.setcash(args.cash)
    cerebro.broker.setcommission(commission=args.commission)

    start_value = cerebro.broker.getvalue()
    print("Backtrader SMA Crossover Demo")
    print(f"data={args.data}")
    print(
        f"params: fast_ma={args.fast}, slow_ma={args.slow}, "
        f"cash={args.cash:.2f}, stake={args.stake}, "
        f"commission={args.commission:.4f}"
    )
    print(f"start_value={start_value:.2f}")

    cerebro.run()

    end_value = cerebro.broker.getvalue()
    total_return = (end_value / start_value - 1.0) * 100
    print(f"end_value={end_value:.2f}")
    print(f"total_return={total_return:.2f}%")


def main() -> None:
    args = parse_args()
    validate_args(args)
    run_backtest(args)


if __name__ == "__main__":
    main()

