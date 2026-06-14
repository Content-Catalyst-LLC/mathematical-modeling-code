from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from mathematical_modeling_in_ecology_and_sustainability.core import (
    build_sustainability_review_card,
    ecology_priority,
    evaluate_scenario,
    load_ecology_model_records,
    load_resource_scenarios,
    simulate_resource,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run mathematical modeling in ecology and sustainability workflow.")
    parser.add_argument("--register-file", type=Path, default=Path("data/ecology_model_register.csv"))
    parser.add_argument("--scenarios-file", type=Path, default=Path("data/resource_scenarios.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"
    logs_dir = args.output_dir / "logs"

    records = load_ecology_model_records(args.register_file)
    scenarios = load_resource_scenarios(args.scenarios_file)

    register_rows = [
        {**asdict(record), "ecology_priority": ecology_priority(record)}
        for record in records
    ]
    scenario_rows = [evaluate_scenario(scenario) for scenario in scenarios]
    baseline_trajectory = simulate_resource(scenarios[0])

    write_csv(tables_dir / "ecology_model_register.csv", register_rows)
    write_csv(tables_dir / "sustainability_scenario_review.csv", scenario_rows)
    write_csv(tables_dir / "baseline_resource_trajectory.csv", baseline_trajectory)

    write_json(
        json_dir / "sustainability_review_card.json",
        build_sustainability_review_card(register_rows, scenario_rows),
    )

    logs_dir.mkdir(parents=True, exist_ok=True)
    (logs_dir / "ecology_sustainability_run.log").write_text(
        "Mathematical modeling in ecology and sustainability workflow completed successfully.\n",
        encoding="utf-8",
    )

    print("Ecology and sustainability workflow complete.")
    print(f"Records: {len(records)}")
    print(f"Scenarios: {len(scenarios)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
