from pathlib import Path

from quant_open_source_lab.config import BacktestConfig
from quant_open_source_lab.engines.backtrader_engine import run_backtest


def test_backtrader_smoke_returns_structured_result() -> None:
    result = run_backtest(
        BacktestConfig(
            Path("projects/backtrader/examples/data/synthetic_ohlcv.csv"),
            fast=3,
            slow=5,
        )
    )
    assert result.engine == "backtrader"
    expected_metrics = {"total_return", "max_drawdown", "trade_count", "fees"}
    assert expected_metrics <= result.metrics.keys()
    assert list(result.trades.columns) == [
        "date",
        "side",
        "price",
        "size",
        "commission",
    ]
    assert not result.equity.empty
