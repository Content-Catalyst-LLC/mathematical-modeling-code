from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from ai_assisted_modeling_and_human_judgment.core import (
    build_ai_assisted_modeling_governance_card,
    evaluate_judgment_case,
    load_ai_assistance_records,
    load_human_judgment_cases,
    review_priority,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run AI-assisted modeling and human judgment workflow.")
    parser.add_argument("--assistance-file", type=Path, default=Path("data/ai_assistance_register.csv"))
    parser.add_argument("--judgment-file", type=Path, default=Path("data/human_judgment_cases.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"
    logs_dir = args.output_dir / "logs"

    assistance_records = load_ai_assistance_records(args.assistance_file)
    judgment_cases = load_human_judgment_cases(args.judgment_file)

    assistance_rows = [
        {**asdict(record), "review_priority": review_priority(record)}
        for record in assistance_records
    ]
    judgment_rows = [evaluate_judgment_case(case) for case in judgment_cases]

    write_csv(tables_dir / "ai_assistance_register.csv", assistance_rows)
    write_csv(tables_dir / "human_judgment_review.csv", judgment_rows)

    write_json(
        json_dir / "ai_assisted_modeling_governance_card.json",
        build_ai_assisted_modeling_governance_card(assistance_rows, judgment_rows),
    )

    logs_dir.mkdir(parents=True, exist_ok=True)
    (logs_dir / "ai_assisted_modeling_run.log").write_text(
        "AI-assisted modeling and human judgment workflow completed successfully.\n",
        encoding="utf-8",
    )

    print("AI-assisted modeling and human judgment workflow complete.")
    print(f"AI assistance records: {len(assistance_records)}")
    print(f"Human judgment cases: {len(judgment_cases)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
