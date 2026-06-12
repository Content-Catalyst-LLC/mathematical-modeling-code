from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from simulation_computational_modeling.core import (
    build_simulation_audit_card,
    load_records,
    load_scenarios,
    simulate,
    simulation_risk_score,
    summarize,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the simulation and computational modeling workflow.")
    parser.add_argument("--scenario-file", type=Path, default=Path("data/simulation_scenarios.csv"))
    parser.add_argument("--register-file", type=Path, default=Path("data/simulation_model_register.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"

    scenarios = load_scenarios(args.scenario_file)
    records = load_records(args.register_file)

    rows: list[dict[str, object]] = []
    for scenario in scenarios:
        for seed in range(1, scenario.replications + 1):
            rows.extend(simulate(scenario, seed))

    summary_rows = summarize(rows)

    register_rows = [
        {**asdict(record), "simulation_risk_score": simulation_risk_score(record)}
        for record in records
    ]

    write_csv(tables_dir / "simulation_trajectories.csv", rows)
    write_csv(tables_dir / "simulation_scenario_summary.csv", summary_rows)
    write_csv(tables_dir / "simulation_model_register.csv", register_rows)
    write_json(json_dir / "simulation_audit_card.json", build_simulation_audit_card(records, scenarios, summary_rows))

    print("Simulation and computational modeling workflow complete.")
    print(f"Simulation records: {len(records)}")
    print(f"Scenarios: {len(scenarios)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
