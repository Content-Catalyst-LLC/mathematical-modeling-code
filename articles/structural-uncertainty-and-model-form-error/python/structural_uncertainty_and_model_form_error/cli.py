from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from structural_uncertainty_and_model_form_error.core import (
    build_structural_uncertainty_assessment_card,
    comparison_rows,
    load_model_forms,
    load_records,
    structural_risk_score,
    structural_summary,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run structural uncertainty and model-form comparison workflow.")
    parser.add_argument("--forms-file", type=Path, default=Path("data/model_forms.csv"))
    parser.add_argument("--register-file", type=Path, default=Path("data/structural_uncertainty_register.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"
    logs_dir = args.output_dir / "logs"

    forms = load_model_forms(args.forms_file)
    records = load_records(args.register_file)
    rows = comparison_rows(forms)

    register_rows = [
        {**asdict(record), "structural_risk_score": structural_risk_score(record)}
        for record in records
    ]

    write_csv(tables_dir / "model_forms.csv", [asdict(item) for item in forms])
    write_csv(tables_dir / "model_form_comparison.csv", rows)
    write_csv(tables_dir / "structural_uncertainty_register.csv", register_rows)

    write_json(
        json_dir / "structural_uncertainty_assessment_card.json",
        build_structural_uncertainty_assessment_card(rows, register_rows),
    )

    logs_dir.mkdir(parents=True, exist_ok=True)
    (logs_dir / "structural_uncertainty_run.log").write_text(
        "Structural uncertainty and model-form comparison workflow completed successfully.\n",
        encoding="utf-8",
    )

    print("Structural uncertainty workflow complete.")
    print(f"Summary: {structural_summary(rows)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
