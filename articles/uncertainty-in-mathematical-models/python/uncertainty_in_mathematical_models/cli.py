from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from uncertainty_in_mathematical_models.core import (
    build_uncertainty_assessment_card,
    load_parameters,
    load_records,
    output_summary,
    propagation_rows,
    uncertainty_risk_score,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run uncertainty propagation and review workflow.")
    parser.add_argument("--parameters-file", type=Path, default=Path("data/uncertain_parameters.csv"))
    parser.add_argument("--register-file", type=Path, default=Path("data/uncertainty_register.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"
    logs_dir = args.output_dir / "logs"

    parameters = load_parameters(args.parameters_file)
    records = load_records(args.register_file)

    rows = propagation_rows(parameters)
    register_rows = [
        {**asdict(record), "uncertainty_risk_score": uncertainty_risk_score(record)}
        for record in records
    ]

    write_csv(tables_dir / "uncertain_parameters.csv", [asdict(item) for item in parameters])
    write_csv(tables_dir / "uncertainty_propagation_runs.csv", rows)
    write_csv(tables_dir / "uncertainty_register.csv", register_rows)

    write_json(
        json_dir / "uncertainty_assessment_card.json",
        build_uncertainty_assessment_card(rows, register_rows),
    )

    logs_dir.mkdir(parents=True, exist_ok=True)
    (logs_dir / "uncertainty_run.log").write_text(
        "Uncertainty propagation workflow completed successfully.\n",
        encoding="utf-8",
    )

    print("Uncertainty propagation workflow complete.")
    print(f"Output summary: {output_summary(rows)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
