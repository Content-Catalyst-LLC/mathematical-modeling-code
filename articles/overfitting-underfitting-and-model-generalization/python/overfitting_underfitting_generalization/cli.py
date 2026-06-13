from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from overfitting_underfitting_generalization.core import (
    build_generalization_assessment_card,
    generalization_risk_score,
    load_models,
    load_records,
    model_rows,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run overfitting, underfitting, and generalization diagnostics.")
    parser.add_argument("--models-file", type=Path, default=Path("data/generalization_models.csv"))
    parser.add_argument("--register-file", type=Path, default=Path("data/generalization_register.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"
    logs_dir = args.output_dir / "logs"

    models = load_models(args.models_file)
    records = load_records(args.register_file)

    ranked = model_rows(models)
    register_rows = [
        {**asdict(record), "generalization_risk_score": generalization_risk_score(record)}
        for record in records
    ]

    write_csv(tables_dir / "generalization_model_diagnostics.csv", ranked)
    write_csv(tables_dir / "generalization_register.csv", register_rows)
    write_json(json_dir / "generalization_assessment_card.json", build_generalization_assessment_card(ranked, register_rows))

    logs_dir.mkdir(parents=True, exist_ok=True)
    (logs_dir / "generalization_run.log").write_text(
        "Overfitting, underfitting, and generalization workflow completed successfully.\n",
        encoding="utf-8",
    )

    print("Generalization workflow complete.")
    print(f"Selected for review: {ranked[0]['model_id']}")
    print(f"Model count: {len(ranked)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
