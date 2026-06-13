from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from sensitivity_analysis_and_robustness.core import (
    baseline_output,
    build_robustness_assessment_card,
    load_parameters,
    load_records,
    sensitivity_risk_score,
    sensitivity_summary,
    sweep_rows,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run sensitivity analysis and robustness workflow.")
    parser.add_argument("--parameters-file", type=Path, default=Path("data/sensitivity_parameters.csv"))
    parser.add_argument("--register-file", type=Path, default=Path("data/sensitivity_register.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"
    logs_dir = args.output_dir / "logs"

    params = load_parameters(args.parameters_file)
    records = load_records(args.register_file)

    sweep = sweep_rows(params)
    summary = sensitivity_summary(sweep)
    register_rows = [
        {**asdict(record), "sensitivity_risk_score": sensitivity_risk_score(record)}
        for record in records
    ]

    write_csv(tables_dir / "sensitivity_parameters.csv", [asdict(item) for item in params])
    write_csv(tables_dir / "sensitivity_parameter_sweep.csv", sweep)
    write_csv(tables_dir / "sensitivity_summary.csv", summary)
    write_csv(tables_dir / "sensitivity_register.csv", register_rows)

    write_json(
        json_dir / "robustness_assessment_card.json",
        build_robustness_assessment_card(params, sweep, summary, register_rows),
    )

    logs_dir.mkdir(parents=True, exist_ok=True)
    (logs_dir / "sensitivity_run.log").write_text(
        "Sensitivity analysis and robustness workflow completed successfully.\n",
        encoding="utf-8",
    )

    print("Sensitivity and robustness workflow complete.")
    print(f"Baseline output: {baseline_output(params)}")
    print(f"Most sensitive parameter: {summary[0]['parameter']}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
