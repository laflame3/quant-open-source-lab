"""Structured engine results used instead of stdout-only evidence."""

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class BacktestResult:
    engine: str
    metrics: dict[str, float]
    equity: pd.DataFrame
    trades: pd.DataFrame


@dataclass(frozen=True)
class ComparisonResult:
    """Machine-readable comparison without asserting identical engine behavior."""

    assumptions: dict[str, str]
    metrics: pd.DataFrame
    trade_summary: pd.DataFrame
