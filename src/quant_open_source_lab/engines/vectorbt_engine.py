"""Vectorbt adapter using the same inputs, signal, sizing, fees, and metrics."""

import numpy as np
import pandas as pd
import vectorbt as vbt

from quant_open_source_lab.config import BacktestConfig
from quant_open_source_lab.data import load_ohlcv
from quant_open_source_lab.metrics import performance_metrics
from quant_open_source_lab.schemas import BacktestResult
from quant_open_source_lab.signals import sma_target


def run_backtest(config: BacktestConfig) -> BacktestResult:
    """Run a fixed-share long/cash portfolio.

    The target at row ``t`` was computed from closes through ``t-1`` and is
    therefore executed at row ``t`` open. This is the same next-bar convention
    used by the event-driven adapter.
    """
    config.validate()
    frame = load_ohlcv(config.data_path)
    target = sma_target(frame["close"], config.fast, config.slow)
    delta = target.diff().fillna(target).astype(float)
    orders = delta * float(config.stake)
    portfolio = vbt.Portfolio.from_orders(
        close=frame["open"],
        size=orders,
        size_type="amount",
        fees=config.commission,
        init_cash=config.cash,
        freq="1D",
    )
    equity_series = portfolio.value()
    equity = pd.DataFrame(
        {
            "date": frame.index.strftime("%Y-%m-%d"),
            "equity": equity_series.to_numpy(dtype=float),
            "position": target.to_numpy(dtype=float) * config.stake,
        }
    )
    records = portfolio.orders.records_readable
    if records.empty:
        trades = pd.DataFrame(
            columns=["date", "side", "price", "size", "commission"]
        )
    else:
        dates = pd.to_datetime(records["Timestamp"], errors="raise")
        trades = pd.DataFrame(
            {
                "date": dates.dt.strftime("%Y-%m-%d"),
                "side": records["Side"].str.lower().to_numpy(),
                "price": records["Price"].to_numpy(dtype=float),
                "size": np.where(
                    records["Side"].eq("Sell"),
                    -records["Size"],
                    records["Size"],
                ).astype(float),
                "commission": records["Fees"].to_numpy(dtype=float),
            }
        )
    metrics = performance_metrics(equity["equity"])
    metrics.update(
        {
            "trade_count": float(len(trades)),
            "fees": float(trades["commission"].sum()) if not trades.empty else 0.0,
        }
    )
    return BacktestResult("vectorbt", metrics, equity, trades)
