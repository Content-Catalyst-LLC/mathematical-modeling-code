from __future__ import annotations

import argparse
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from what_is_calculus_for_systems_modeling.core import (
    load_scenarios,
    scenario_manifest,
    simulate_logistic,
    summarize_runs,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run calculus systems modeling example.")
    parser.add_argument("--scenario-file", type=Path, default=Path("data/system_scenarios.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    scenarios = load_scenarios(args.scenario_file)

    rows: list[dict[str, object]] = []
    for scenario in scenarios:
        rows.extend(simulate_logistic(scenario))

    summary = summarize_runs(rows)

    trajectory_path = args.output_dir / "tables" / "calculus_system_trajectories.csv"
    summary_path = args.output_dir / "tables" / "calculus_system_summary.csv"
    manifest_path = args.output_dir / "json" / "calculus_system_manifest.json"
    log_path = args.output_dir / "logs" / "python_workflow.log"

    write_csv(trajectory_path, rows)
    write_csv(summary_path, summary)
    write_json(manifest_path, scenario_manifest(scenarios, summary))

    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("Python calculus systems modeling workflow completed.\n", encoding="utf-8")

    print("Python calculus systems modeling workflow complete.")
    print(f"Scenarios: {len(scenarios)}")
    print(f"Rows: {len(rows)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
