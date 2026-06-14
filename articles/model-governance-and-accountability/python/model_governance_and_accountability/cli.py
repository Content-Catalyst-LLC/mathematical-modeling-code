from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from model_governance_and_accountability.core import (
    build_model_governance_card,
    evaluate_governance_risk,
    governance_priority,
    governance_summary,
    load_governance_register,
    load_governance_risk_cases,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run model governance and accountability workflow.")
    parser.add_argument("--register-file", type=Path, default=Path("data/model_governance_register.csv"))
    parser.add_argument("--risk-file", type=Path, default=Path("data/model_governance_risk_cases.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"
    logs_dir = args.output_dir / "logs"

    register = load_governance_register(args.register_file)
    risk_cases = load_governance_risk_cases(args.risk_file)

    register_rows = [
        {**asdict(record), "governance_priority": governance_priority(record)}
        for record in register
    ]
    risk_rows = [evaluate_governance_risk(case) for case in risk_cases]

    write_csv(tables_dir / "model_governance_register.csv", register_rows)
    write_csv(tables_dir / "model_governance_risk_review.csv", risk_rows)

    write_json(
        json_dir / "model_governance_card.json",
        build_model_governance_card(register_rows, risk_rows),
    )

    logs_dir.mkdir(parents=True, exist_ok=True)
    (logs_dir / "model_governance_run.log").write_text(
        "Model governance and accountability workflow completed successfully.\n",
        encoding="utf-8",
    )

    print("Model governance and accountability workflow complete.")
    print(f"Governance register records: {len(register)}")
    print(f"Governance risk cases: {len(risk_cases)}")
    print(f"Governance summary: {governance_summary(risk_rows)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
