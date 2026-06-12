from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from model_comparison_and_selection.core import (
    build_selection_audit_card,
    load_candidates,
    load_records,
    model_rows,
    selection_risk_score,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run model comparison and selection workflow.")
    parser.add_argument("--candidates-file", type=Path, default=Path("data/model_candidates.csv"))
    parser.add_argument("--register-file", type=Path, default=Path("data/model_selection_register.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"
    logs_dir = args.output_dir / "logs"

    models = load_candidates(args.candidates_file)
    records = load_records(args.register_file)

    ranked = model_rows(models)
    register_rows = [
        {**asdict(record), "selection_risk_score": selection_risk_score(record)}
        for record in records
    ]

    write_csv(tables_dir / "model_comparison_table.csv", ranked)
    write_csv(tables_dir / "model_selection_register.csv", register_rows)
    write_json(json_dir / "model_selection_audit_card.json", build_selection_audit_card(ranked, register_rows))

    logs_dir.mkdir(parents=True, exist_ok=True)
    (logs_dir / "model_selection_run.log").write_text(
        "Model comparison and selection workflow completed successfully.\n",
        encoding="utf-8",
    )

    print("Model comparison and selection workflow complete.")
    print(f"Selected model: {ranked[0]['model_id']}")
    print(f"Candidate count: {len(ranked)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
