from pathlib import Path

import pandas as pd
import pytest

from quant_open_source_lab.data import load_ohlcv


def test_loads_repository_fixture() -> None:
    path = Path("projects/backtrader/examples/data/synthetic_ohlcv.csv")
    frame = load_ohlcv(path)
    assert frame.index.is_monotonic_increasing
    assert not frame.empty


def test_rejects_duplicate_dates(tmp_path: Path) -> None:
    path = tmp_path / "bad.csv"
    pd.DataFrame(
        {
            "date": ["2024-01-01", "2024-01-01"],
            "open": [1, 1],
            "high": [2, 2],
            "low": [0.5, 0.5],
            "close": [1, 1],
            "volume": [1, 1],
        }
    ).to_csv(path, index=False)
    with pytest.raises(ValueError, match="unique"):
        load_ohlcv(path)
