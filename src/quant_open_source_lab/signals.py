"""Engine-independent signal definitions."""

import pandas as pd


def sma_target(close: pd.Series, fast: int, slow: int) -> pd.Series:
    """Return a long/cash target known at each bar close.

    Engines must execute this target no earlier than the next bar. The one-bar
    shift here makes that timing explicit and testable.
    """
    observed = (close.rolling(fast).mean() > close.rolling(slow).mean()).astype(int)
    return observed.shift(1, fill_value=0).rename("target")
