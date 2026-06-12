from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from state_variables_system_representation.core import (
    build_state_audit_card,
    load_representation_scenarios,
    load_state_variables,
    simulate_representation,
    state_risk_score,
    summarize_representation,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the state variables and system representation workflow.")
    parser.add_argument("--state-file", type=Path, default=Path("data/state_variable_register.csv"))
    parser.add_argument("--scenario-file", type=Path, default=Path("data/representation_scenarios.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"

    state_variables = load_state_variables(args.state_file)
    scenarios = load_representation_scenarios(args.scenario_file)

    all_rows = []
    summary_rows = []

    for scenario in scenarios:
        rows = simulate_representation(scenario)
        all_rows.extend(rows)
        summary = summarize_representation(rows)
        summary["description"] = scenario.description
        summary_rows.append(summary)

    state_rows = [
        {
            **asdict(item),
            "state_risk_score": state_risk_score(item),
        }
        for item in state_variables
    ]

    write_csv(tables_dir / "state_representation_timeseries.csv", all_rows)
    write_csv(tables_dir / "state_representation_summary.csv", summary_rows)
    write_csv(tables_dir / "state_variable_register.csv", state_rows)
    write_json(json_dir / "state_representation_audit_card.json", build_state_audit_card(state_variables, summary_rows))

    print("State variables and system representation workflow complete.")
    print(f"State variables: {len(state_variables)}")
    print(f"Scenarios: {len(scenarios)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
