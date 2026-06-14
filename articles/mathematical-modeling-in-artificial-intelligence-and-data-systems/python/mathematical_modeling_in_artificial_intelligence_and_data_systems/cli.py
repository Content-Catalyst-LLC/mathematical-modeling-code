from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from mathematical_modeling_in_artificial_intelligence_and_data_systems.core import (
    build_ai_model_governance_card,
    evaluate_candidate,
    load_ai_model_records,
    load_model_candidates,
    model_priority,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run mathematical modeling in AI and data systems workflow.")
    parser.add_argument("--register-file", type=Path, default=Path("data/ai_model_register.csv"))
    parser.add_argument("--candidates-file", type=Path, default=Path("data/model_candidates.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"
    logs_dir = args.output_dir / "logs"

    records = load_ai_model_records(args.register_file)
    candidates = load_model_candidates(args.candidates_file)

    register_rows = [
        {**asdict(record), "model_priority": model_priority(record)}
        for record in records
    ]
    candidate_rows = [evaluate_candidate(candidate) for candidate in candidates]

    write_csv(tables_dir / "ai_model_register.csv", register_rows)
    write_csv(tables_dir / "ai_model_candidate_review.csv", candidate_rows)

    write_json(
        json_dir / "ai_model_governance_card.json",
        build_ai_model_governance_card(register_rows, candidate_rows),
    )

    logs_dir.mkdir(parents=True, exist_ok=True)
    (logs_dir / "ai_data_systems_run.log").write_text(
        "Mathematical modeling in artificial intelligence and data systems workflow completed successfully.\n",
        encoding="utf-8",
    )

    print("AI and data systems workflow complete.")
    print(f"Records: {len(records)}")
    print(f"Candidates: {len(candidates)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
