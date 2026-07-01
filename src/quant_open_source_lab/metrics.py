"""Small, transparent performance metric helpers."""

import numpy as np
import pandas as pd


def performance_metrics(equity: pd.Series) -> dict[str, float]:
    if equity.empty or equity.iloc[0] <= 0:
        raise ValueError("Equity must be non-empty and start positive")
    returns = equity.pct_change().dropna()
    total_return = float(equity.iloc[-1] / equity.iloc[0] - 1)
    drawdown = equity / equity.cummax() - 1
    volatility = float(returns.std(ddof=1)) if len(returns) > 1 else 0.0
    sharpe = float(np.sqrt(252) * returns.mean() / volatility) if volatility else 0.0
    return {
        "total_return": total_return,
        "sharpe_annualized_252": sharpe,
        "max_drawdown": float(drawdown.min()),
    }
