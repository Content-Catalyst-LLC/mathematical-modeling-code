from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from assumptions_model_design.core import (
    assumption_risk_score,
    build_model_design_card,
    load_assumptions,
    load_scenarios,
    simulate_resource,
    summarize_resource,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the assumptions and model design companion workflow.")
    parser.add_argument("--assumption-file", type=Path, default=Path("data/assumption_register.csv"))
    parser.add_argument("--scenario-file", type=Path, default=Path("data/resource_scenarios.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"

    assumptions = load_assumptions(args.assumption_file)
    scenarios = load_scenarios(args.scenario_file)

    all_rows = []
    summary_rows = []

    for scenario in scenarios:
        rows = simulate_resource(scenario)
        all_rows.extend(rows)
        summary = summarize_resource(rows)
        summary["description"] = scenario.description
        summary_rows.append(summary)

    assumption_rows = [
        {
            **asdict(item),
            "assumption_risk_score": assumption_risk_score(item),
        }
        for item in assumptions
    ]

    write_csv(tables_dir / "resource_scenario_timeseries.csv", all_rows)
    write_csv(tables_dir / "resource_scenario_summary.csv", summary_rows)
    write_csv(tables_dir / "assumption_register.csv", assumption_rows)
    write_json(json_dir / "model_design_card.json", build_model_design_card(assumptions, summary_rows))

    print("Assumption-aware model design workflow complete.")
    print(f"Assumptions: {len(assumptions)}")
    print(f"Scenarios: {len(scenarios)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
