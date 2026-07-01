from pathlib import Path

import pytest

from quant_open_source_lab.config import BacktestConfig


def test_rejects_inverted_windows(tmp_path: Path) -> None:
    path = tmp_path / "data.csv"
    path.touch()
    with pytest.raises(ValueError, match="fast"):
        BacktestConfig(path, fast=30, slow=10).validate()
