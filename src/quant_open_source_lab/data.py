"""OHLCV loading and strict validation."""

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = ("date", "open", "high", "low", "close", "volume")


def load_ohlcv(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    missing = set(REQUIRED_COLUMNS) - set(frame.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    frame = frame.loc[:, REQUIRED_COLUMNS].copy()
    frame["date"] = pd.to_datetime(frame["date"], errors="raise")
    if frame["date"].duplicated().any() or not frame["date"].is_monotonic_increasing:
        raise ValueError("Dates must be unique and increasing")
    prices = frame[["open", "high", "low", "close"]]
    if prices.isna().any().any() or (prices <= 0).any().any():
        raise ValueError("OHLC prices must be finite and positive")
    if (frame["volume"] < 0).any() or frame["volume"].isna().any():
        raise ValueError("Volume must be non-negative")
    if (frame["high"] < prices[["open", "close", "low"]].max(axis=1)).any():
        raise ValueError("High violates OHLC relationship")
    if (frame["low"] > prices[["open", "close", "high"]].min(axis=1)).any():
        raise ValueError("Low violates OHLC relationship")
    return frame.set_index("date")
