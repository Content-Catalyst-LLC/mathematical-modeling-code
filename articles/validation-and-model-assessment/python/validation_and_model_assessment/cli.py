from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from validation_and_model_assessment.core import (
    build_model_assessment_card,
    classify_fitness,
    error_rows,
    load_observations,
    load_records,
    metric_summary,
    scenario_summary,
    validation_risk_score,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run validation and model assessment workflow.")
    parser.add_argument("--register-file", type=Path, default=Path("data/validation_register.csv"))
    parser.add_argument("--observations-file", type=Path, default=Path("data/validation_observations.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"
    logs_dir = args.output_dir / "logs"

    records = load_records(args.register_file)
    observations = load_observations(args.observations_file)

    errors = error_rows(observations)
    overall = metric_summary(errors)
    by_scenario = scenario_summary(errors)
    register_rows = [
        {**asdict(record), "validation_risk_score": validation_risk_score(record)}
        for record in records
    ]

    write_csv(tables_dir / "validation_observations.csv", [asdict(obs) for obs in observations])
    write_csv(tables_dir / "validation_error_diagnostics.csv", errors)
    write_csv(tables_dir / "validation_scenario_summary.csv", by_scenario)
    write_csv(tables_dir / "validation_register.csv", register_rows)
    write_json(json_dir / "model_assessment_card.json", build_model_assessment_card(records, overall, by_scenario))

    logs_dir.mkdir(parents=True, exist_ok=True)
    (logs_dir / "validation_run.log").write_text(
        "Validation and model assessment workflow completed successfully.\n",
        encoding="utf-8",
    )

    print("Validation and model assessment workflow complete.")
    print(f"Overall metrics: {overall}")
    print(f"Fitness for purpose: {classify_fitness(overall)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
