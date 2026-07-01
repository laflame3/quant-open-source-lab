from pathlib import Path

from quant_open_source_lab.compare import compare_engines
from quant_open_source_lab.config import BacktestConfig
from quant_open_source_lab.engines.vectorbt_engine import run_backtest

FIXTURE = Path("projects/backtrader/examples/data/synthetic_ohlcv.csv")


def test_vectorbt_returns_structured_result() -> None:
    result = run_backtest(BacktestConfig(data_path=FIXTURE, fast=10, slow=30))
    assert result.engine == "vectorbt"
    expected = {"total_return", "max_drawdown", "trade_count", "fees"}
    assert expected <= result.metrics.keys()
    assert {"date", "equity", "position"} <= set(result.equity.columns)


def test_compare_reports_both_engines_and_assumptions() -> None:
    comparison = compare_engines(BacktestConfig(data_path=FIXTURE, fast=10, slow=30))
    assert set(comparison.metrics.index) == {"backtrader", "vectorbt"}
    expected_execution = "target changes execute at the next bar open"
    assert comparison.assumptions["execution"] == expected_execution
    returns = comparison.metrics["total_return"]
    assert abs(float(returns["backtrader"] - returns["vectorbt"])) < 0.01
