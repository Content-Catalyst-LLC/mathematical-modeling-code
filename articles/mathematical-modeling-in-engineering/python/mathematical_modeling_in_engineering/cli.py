from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from mathematical_modeling_in_engineering.core import (
    build_engineering_design_review_card,
    engineering_priority,
    evaluate_beam,
    load_beam_designs,
    load_engineering_model_records,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run mathematical modeling in engineering workflow.")
    parser.add_argument("--register-file", type=Path, default=Path("data/engineering_model_register.csv"))
    parser.add_argument("--designs-file", type=Path, default=Path("data/beam_designs.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"
    logs_dir = args.output_dir / "logs"

    records = load_engineering_model_records(args.register_file)
    designs = load_beam_designs(args.designs_file)

    register_rows = [
        {**asdict(record), "engineering_priority": engineering_priority(record)}
        for record in records
    ]
    design_rows = [evaluate_beam(design) for design in designs]

    write_csv(tables_dir / "engineering_model_register.csv", register_rows)
    write_csv(tables_dir / "beam_design_review.csv", design_rows)

    write_json(
        json_dir / "engineering_design_review_card.json",
        build_engineering_design_review_card(register_rows, design_rows),
    )

    logs_dir.mkdir(parents=True, exist_ok=True)
    (logs_dir / "engineering_modeling_run.log").write_text(
        "Mathematical modeling in engineering workflow completed successfully.\n",
        encoding="utf-8",
    )

    print("Engineering modeling workflow complete.")
    print(f"Records: {len(records)}")
    print(f"Designs: {len(designs)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
