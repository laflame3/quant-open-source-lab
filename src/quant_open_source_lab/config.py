"""Experiment configuration and validation."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BacktestConfig:
    data_path: Path
    fast: int = 10
    slow: int = 30
    cash: float = 100_000.0
    stake: int = 100
    commission: float = 0.001

    def validate(self) -> None:
        if self.fast <= 0 or self.slow <= 0:
            raise ValueError("SMA windows must be positive")
        if self.fast >= self.slow:
            raise ValueError("fast SMA window must be smaller than slow")
        if self.cash <= 0 or self.stake <= 0:
            raise ValueError("cash and stake must be positive")
        if self.commission < 0:
            raise ValueError("commission cannot be negative")
        if not self.data_path.is_file():
            raise FileNotFoundError(f"Data file not found: {self.data_path}")
