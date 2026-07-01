"""Structured engine results used instead of stdout-only evidence."""

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class BacktestResult:
    engine: str
    metrics: dict[str, float]
    equity: pd.DataFrame
    trades: pd.DataFrame
