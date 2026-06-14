from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from mathematical_modeling_in_science.core import (
    build_scientific_model_evidence_card,
    load_population_scenarios,
    load_scientific_model_records,
    logistic_population,
    scenario_summary,
    scientific_priority,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run mathematical modeling in science workflow.")
    parser.add_argument("--register-file", type=Path, default=Path("data/scientific_model_register.csv"))
    parser.add_argument("--scenarios-file", type=Path, default=Path("data/population_scenarios.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"
    logs_dir = args.output_dir / "logs"

    records = load_scientific_model_records(args.register_file)
    scenarios = load_population_scenarios(args.scenarios_file)

    register_rows = [
        {**asdict(record), "scientific_priority": scientific_priority(record)}
        for record in records
    ]
    scenario_rows = [scenario_summary(scenario) for scenario in scenarios]
    baseline_trajectory = logistic_population(40.0, 0.28, 500.0, 20)

    write_csv(tables_dir / "scientific_model_register.csv", register_rows)
    write_csv(tables_dir / "population_scenario_summary.csv", scenario_rows)
    write_csv(tables_dir / "baseline_population_trajectory.csv", baseline_trajectory)

    write_json(
        json_dir / "scientific_model_evidence_card.json",
        build_scientific_model_evidence_card(register_rows, scenario_rows),
    )

    logs_dir.mkdir(parents=True, exist_ok=True)
    (logs_dir / "scientific_modeling_run.log").write_text(
        "Mathematical modeling in science workflow completed successfully.\n",
        encoding="utf-8",
    )

    print("Scientific modeling workflow complete.")
    print(f"Records: {len(records)}")
    print(f"Scenarios: {len(scenarios)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
