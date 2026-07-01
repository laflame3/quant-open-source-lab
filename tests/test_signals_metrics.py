import pandas as pd
import pytest

from quant_open_source_lab.metrics import performance_metrics
from quant_open_source_lab.signals import sma_target


def test_signal_is_lagged_one_bar() -> None:
    close = pd.Series([3.0, 2.0, 1.0, 2.0, 4.0])
    target = sma_target(close, fast=1, slow=3)
    assert target.tolist() == [0, 0, 0, 0, 1]


def test_known_drawdown_and_return() -> None:
    metrics = performance_metrics(pd.Series([100.0, 120.0, 90.0]))
    assert metrics["total_return"] == pytest.approx(-0.1)
    assert metrics["max_drawdown"] == pytest.approx(-0.25)
