from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from mathematical_modeling_in_an_age_of_complexity.core import (
    build_complexity_model_review_card,
    evaluate_scenario,
    load_complexity_model_records,
    load_complexity_scenarios,
    model_priority,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run mathematical modeling in an age of complexity workflow.")
    parser.add_argument("--models-file", type=Path, default=Path("data/complexity_model_register.csv"))
    parser.add_argument("--scenarios-file", type=Path, default=Path("data/complexity_scenarios.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"
    logs_dir = args.output_dir / "logs"

    records = load_complexity_model_records(args.models_file)
    scenarios = load_complexity_scenarios(args.scenarios_file)

    model_rows = [
        {**asdict(record), "model_priority": model_priority(record)}
        for record in records
    ]
    scenario_rows = [evaluate_scenario(scenario) for scenario in scenarios]

    write_csv(tables_dir / "complexity_model_register.csv", model_rows)
    write_csv(tables_dir / "complexity_scenario_review.csv", scenario_rows)

    write_json(
        json_dir / "complexity_model_review_card.json",
        build_complexity_model_review_card(model_rows, scenario_rows),
    )

    logs_dir.mkdir(parents=True, exist_ok=True)
    (logs_dir / "complexity_modeling_run.log").write_text(
        "Mathematical modeling in an age of complexity workflow completed successfully.\n",
        encoding="utf-8",
    )

    print("Complexity modeling workflow complete.")
    print(f"Models: {len(records)}")
    print(f"Scenarios: {len(scenarios)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
