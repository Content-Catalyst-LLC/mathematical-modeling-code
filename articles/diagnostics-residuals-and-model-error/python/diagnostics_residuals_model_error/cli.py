from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from diagnostics_residuals_model_error.core import (
    build_diagnostic_assessment_card,
    diagnostic_risk_score,
    error_summary,
    flag_outliers,
    group_summary,
    load_observations,
    load_records,
    residual_rows,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run residual diagnostics and model error workflow.")
    parser.add_argument("--observations-file", type=Path, default=Path("data/diagnostic_observations.csv"))
    parser.add_argument("--register-file", type=Path, default=Path("data/diagnostic_register.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"
    logs_dir = args.output_dir / "logs"

    observations = load_observations(args.observations_file)
    records = load_records(args.register_file)

    rows = residual_rows(observations)
    register_rows = [
        {**asdict(record), "diagnostic_risk_score": diagnostic_risk_score(record)}
        for record in records
    ]
    outliers = flag_outliers(rows)

    write_csv(tables_dir / "diagnostic_observations.csv", [asdict(item) for item in observations])
    write_csv(tables_dir / "residual_diagnostics.csv", rows)
    write_csv(tables_dir / "diagnostic_group_summary.csv", group_summary(rows))
    write_csv(tables_dir / "diagnostic_register.csv", register_rows)

    if outliers:
        write_csv(tables_dir / "diagnostic_outlier_flags.csv", outliers)

    write_json(json_dir / "diagnostic_assessment_card.json", build_diagnostic_assessment_card(rows, register_rows))

    logs_dir.mkdir(parents=True, exist_ok=True)
    (logs_dir / "diagnostic_run.log").write_text(
        "Residual diagnostics and model error workflow completed successfully.\n",
        encoding="utf-8",
    )

    print("Residual diagnostic workflow complete.")
    print(f"Overall error summary: {error_summary(rows)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
