from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from model_interpretation_and_decision_making.core import (
    build_decision_support_review_card,
    evaluate_option,
    interpretation_priority,
    load_decision_options,
    load_interpretation_records,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run model interpretation and decision-making workflow.")
    parser.add_argument("--register-file", type=Path, default=Path("data/interpretation_register.csv"))
    parser.add_argument("--options-file", type=Path, default=Path("data/decision_options.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"
    logs_dir = args.output_dir / "logs"

    records = load_interpretation_records(args.register_file)
    options = load_decision_options(args.options_file)

    register_rows = [
        {**asdict(record), "interpretation_priority": interpretation_priority(record)}
        for record in records
    ]
    option_rows = [evaluate_option(option) for option in options]

    write_csv(tables_dir / "interpretation_register.csv", register_rows)
    write_csv(tables_dir / "decision_option_review.csv", option_rows)

    write_json(
        json_dir / "decision_support_review_card.json",
        build_decision_support_review_card(register_rows, option_rows),
    )

    logs_dir.mkdir(parents=True, exist_ok=True)
    (logs_dir / "decision_interpretation_run.log").write_text(
        "Model interpretation and decision-making workflow completed successfully.\n",
        encoding="utf-8",
    )

    print("Model interpretation and decision workflow complete.")
    print(f"Records: {len(records)}")
    print(f"Options: {len(options)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
