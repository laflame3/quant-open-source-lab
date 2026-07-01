"""Command-line smoke entry point."""

import argparse
import json
from pathlib import Path

from quant_open_source_lab.config import BacktestConfig
from quant_open_source_lab.engines.backtrader_engine import run_backtest

DEFAULT_DATA = Path("projects/backtrader/examples/data/synthetic_ohlcv.csv")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the reproducible Backtrader demo")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--fast", type=int, default=10)
    parser.add_argument("--slow", type=int, default=30)
    parser.add_argument("--cash", type=float, default=100_000)
    parser.add_argument("--stake", type=int, default=100)
    parser.add_argument("--commission", type=float, default=0.001)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run_backtest(
        BacktestConfig(
            data_path=args.data,
            fast=args.fast,
            slow=args.slow,
            cash=args.cash,
            stake=args.stake,
            commission=args.commission,
        )
    )
    if args.output:
        args.output.mkdir(parents=True, exist_ok=True)
        result.equity.to_csv(args.output / "equity.csv", index=False)
        result.trades.to_csv(args.output / "trades.csv", index=False)
        (args.output / "metrics.json").write_text(
            json.dumps(result.metrics, indent=2), encoding="utf-8"
        )
    print(json.dumps(result.metrics, indent=2))


if __name__ == "__main__":
    main()
