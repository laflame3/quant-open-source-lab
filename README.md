# Quant Open Source Lab

A reproducible lab for studying open-source quantitative research and backtesting frameworks.

## Current reproducible scope

The implemented baseline compares callable Backtrader and vectorbt SMA-crossover
engines on the same committed **synthetic** OHLCV fixture. Both paths share
validated inputs, a next-bar execution contract, fixed-share sizing, commission,
and structured outputs. Synthetic results verify software behavior only; they
are not evidence of alpha or expected investment performance.

```powershell
uv sync --locked --group dev
uv run pytest -q
uv run quant-lab backtrader --fast 3 --slow 5 --output artifacts/backtrader-smoke
uv run quant-lab vectorbt --fast 3 --slow 5 --output artifacts/vectorbt-smoke
uv run quant-lab compare --fast 3 --slow 5 --output artifacts/compare-smoke
```

Python 3.11 is pinned in `.python-version`; dependencies are locked by `uv.lock`.
See `AUDIT_EVIDENCE.md` for the exact evidence boundary.

This repository records my long-term learning process around open-source quant tools. It is designed to keep real notes, runnable demos, architecture summaries, pitfalls, and research experiments under version control.

## Learning Goals

- Understand how popular open-source quant frameworks are designed and used.
- Build minimal runnable demos instead of only reading documentation.
- Compare event-driven, vectorized, machine-learning, and production-grade research workflows.
- Connect open-source tools with my own CTA, futures, factor research, and machine learning background.
- Maintain a public GitHub learning portfolio with meaningful commits.

## Current Focus Projects

- Backtrader: event-driven backtesting framework.
- vectorbt: implemented vectorized adapter under the shared baseline contract.
- Qlib, Lean, and OpenBB: documented learning backlog; no runnable integration yet.

## Repository Structure

```text
docs/       Project-level learning methods, framework maps, and terminology.
projects/   Per-framework notes, installation logs, architecture notes, demos, and pitfalls.
examples/   Shared demo data, notebooks, and scripts created during learning.
templates/  Reusable templates for project reviews, install notes, demos, and issue/PR logs.
logs/       Daily learning log and contribution log.
scripts/    Utility scripts for local setup and reproducible workflows.
```

## How To Use

1. Pick one framework from `projects/`.
2. Read its README and official documentation.
3. Record installation steps in `install_notes.md`.
4. Run or create a minimal demo in `examples/`.
5. Summarize architecture and key concepts in `architecture_notes.md`.
6. Record daily progress in `logs/daily_log.md`.
7. Track meaningful learning, demos, issues, PRs, or documentation work in `logs/contribution_log.md`.

## Next Plans

- Explain and regression-test remaining Backtrader/vectorbt execution differences.
- Add source links, documentation links, and reading notes for each framework.
- Compare event-driven and vectorized backtesting from the same simple CTA strategy.
- Explore Qlib after the basic backtesting workflow is stable.
- Build personal CTA / ML / Agent quant research demos based on reusable patterns.

