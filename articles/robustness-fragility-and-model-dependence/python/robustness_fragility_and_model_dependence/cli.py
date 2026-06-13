from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from robustness_fragility_and_model_dependence.core import (
    build_robustness_fragility_assessment_card,
    load_records,
    load_scenarios,
    robustness_risk_score,
    robustness_rows,
    robustness_summary,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run robustness, fragility, and model-dependence workflow.")
    parser.add_argument("--scenarios-file", type=Path, default=Path("data/robustness_scenarios.csv"))
    parser.add_argument("--register-file", type=Path, default=Path("data/robustness_register.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"
    logs_dir = args.output_dir / "logs"

    items = load_scenarios(args.scenarios_file)
    records = load_records(args.register_file)
    rows = robustness_rows(items)

    register_rows = [
        {**asdict(record), "robustness_risk_score": robustness_risk_score(record)}
        for record in records
    ]

    write_csv(tables_dir / "robustness_scenarios.csv", [asdict(item) for item in items])
    write_csv(tables_dir / "robustness_matrix.csv", rows)
    write_csv(tables_dir / "robustness_register.csv", register_rows)

    write_json(
        json_dir / "robustness_fragility_assessment_card.json",
        build_robustness_fragility_assessment_card(rows, register_rows),
    )

    logs_dir.mkdir(parents=True, exist_ok=True)
    (logs_dir / "robustness_run.log").write_text(
        "Robustness, fragility, and model-dependence workflow completed successfully.\n",
        encoding="utf-8",
    )

    print("Robustness and fragility workflow complete.")
    print(f"Summary: {robustness_summary(rows)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
