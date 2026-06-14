from __future__ import annotations

import argparse
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from future_directions_in_mathematical_modeling.core import (
    build_future_modeling_review_card,
    direction_priority,
    load_future_modeling_directions,
    portfolio_summary,
    write_csv,
    write_json,
)


def parse_args():
    parser = argparse.ArgumentParser(description="Run future directions in mathematical modeling workflow.")
    parser.add_argument("--directions-file", type=Path, default=Path("data/future_modeling_directions.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = [direction_priority(row) for row in load_future_modeling_directions(args.directions_file)]
    write_csv(args.output_dir / "tables" / "future_modeling_direction_register.csv", rows)
    write_json(args.output_dir / "json" / "future_modeling_review_card.json", build_future_modeling_review_card(rows))
    (args.output_dir / "logs").mkdir(parents=True, exist_ok=True)
    (args.output_dir / "logs" / "future_modeling_run.log").write_text("Workflow completed successfully.\n", encoding="utf-8")
    print("Future directions in mathematical modeling workflow complete.")
    print(f"Portfolio summary: {portfolio_summary(rows)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
