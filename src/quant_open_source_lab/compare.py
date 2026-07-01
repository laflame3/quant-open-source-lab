"""Engine comparison with an explicit, stable output schema."""

import pandas as pd

from quant_open_source_lab.config import BacktestConfig
from quant_open_source_lab.engines.backtrader_engine import run_backtest as run_bt
from quant_open_source_lab.engines.vectorbt_engine import run_backtest as run_vbt
from quant_open_source_lab.schemas import ComparisonResult

ASSUMPTIONS = {
    "signal": "SMA state is observed at bar close",
    "execution": "target changes execute at the next bar open",
    "sizing": "fixed shares; long or cash only",
    "fees": "proportional commission; no slippage",
    "evidence": "synthetic fixture validates software behavior, not alpha",
}


def compare_engines(config: BacktestConfig) -> ComparisonResult:
    results = [run_bt(config), run_vbt(config)]
    metric_rows = []
    trade_rows = []
    for result in results:
        metric_rows.append({"engine": result.engine, **result.metrics})
        trade_rows.append(
            {
                "engine": result.engine,
                "trade_count": len(result.trades),
                "first_trade_date": (
                    str(result.trades.iloc[0]["date"])
                    if not result.trades.empty
                    else None
                ),
                "last_trade_date": (
                    str(result.trades.iloc[-1]["date"])
                    if not result.trades.empty
                    else None
                ),
            }
        )
    return ComparisonResult(
        ASSUMPTIONS,
        pd.DataFrame(metric_rows).set_index("engine"),
        pd.DataFrame(trade_rows).set_index("engine"),
    )
