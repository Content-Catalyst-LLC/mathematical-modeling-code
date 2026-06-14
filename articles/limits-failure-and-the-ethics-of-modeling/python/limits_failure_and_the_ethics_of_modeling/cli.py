from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from limits_failure_and_the_ethics_of_modeling.core import (
    build_model_ethics_governance_card,
    evaluate_risk_case,
    failure_priority,
    load_failure_records,
    load_risk_cases,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run limits, failure, and ethics of modeling workflow.")
    parser.add_argument("--failures-file", type=Path, default=Path("data/model_failure_register.csv"))
    parser.add_argument("--risk-cases-file", type=Path, default=Path("data/model_ethics_risk_cases.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"
    logs_dir = args.output_dir / "logs"

    failures = load_failure_records(args.failures_file)
    risk_cases = load_risk_cases(args.risk_cases_file)

    failure_rows = [
        {**asdict(record), "failure_priority": failure_priority(record)}
        for record in failures
    ]
    risk_rows = [evaluate_risk_case(case) for case in risk_cases]

    write_csv(tables_dir / "model_failure_register.csv", failure_rows)
    write_csv(tables_dir / "model_ethics_risk_review.csv", risk_rows)

    write_json(
        json_dir / "model_ethics_governance_card.json",
        build_model_ethics_governance_card(failure_rows, risk_rows),
    )

    logs_dir.mkdir(parents=True, exist_ok=True)
    (logs_dir / "limits_failure_ethics_run.log").write_text(
        "Limits, failure, and ethics workflow completed successfully.\n",
        encoding="utf-8",
    )

    print("Model ethics and failure workflow complete.")
    print(f"Failures: {len(failures)}")
    print(f"Risk cases: {len(risk_cases)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
