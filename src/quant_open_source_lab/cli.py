"""Command-line entry points for individual and comparison smoke runs."""

import argparse
import json
from pathlib import Path

from quant_open_source_lab.compare import compare_engines
from quant_open_source_lab.config import BacktestConfig
from quant_open_source_lab.engines.backtrader_engine import run_backtest as run_bt
from quant_open_source_lab.engines.vectorbt_engine import run_backtest as run_vbt

DEFAULT_DATA = Path("projects/backtrader/examples/data/synthetic_ohlcv.csv")


def _write_result(result, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    result.equity.to_csv(output / "equity.csv", index=False)
    result.trades.to_csv(output / "trades.csv", index=False)
    (output / "metrics.json").write_text(
        json.dumps(result.metrics, indent=2), encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run reproducible engine demos")
    parser.add_argument(
        "engine",
        nargs="?",
        choices=["backtrader", "vectorbt", "compare"],
        default="backtrader",
    )
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--fast", type=int, default=10)
    parser.add_argument("--slow", type=int, default=30)
    parser.add_argument("--cash", type=float, default=100_000)
    parser.add_argument("--stake", type=int, default=100)
    parser.add_argument("--commission", type=float, default=0.001)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    config = BacktestConfig(
        args.data,
        args.fast,
        args.slow,
        args.cash,
        args.stake,
        args.commission,
    )
    if args.engine == "compare":
        comparison = compare_engines(config)
        payload = {
            "schema_version": 1,
            "assumptions": comparison.assumptions,
            "metrics": comparison.metrics.reset_index().to_dict("records"),
            "trade_summary": comparison.trade_summary.reset_index().to_dict("records"),
        }
        if args.output:
            args.output.mkdir(parents=True, exist_ok=True)
            (args.output / "comparison.json").write_text(
                json.dumps(payload, indent=2), encoding="utf-8"
            )
        print(json.dumps(payload, indent=2))
        return
    result = run_bt(config) if args.engine == "backtrader" else run_vbt(config)
    if args.output:
        _write_result(result, args.output)
    print(json.dumps(result.metrics, indent=2))


if __name__ == "__main__":
    main()
