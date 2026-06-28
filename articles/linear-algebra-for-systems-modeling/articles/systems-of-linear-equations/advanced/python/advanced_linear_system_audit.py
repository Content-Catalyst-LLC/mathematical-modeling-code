from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedLinearSystemReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedLinearSystemReview]:
    return [
        AdvancedLinearSystemReview("equation_meaning", "required", "Document the real-world meaning of every equation row."),
        AdvancedLinearSystemReview("variable_meaning", "required", "Document each unknown and its feasible range."),
        AdvancedLinearSystemReview("rhs_targets", "required", "Record whether right-hand-side values are targets, observations, or balances."),
        AdvancedLinearSystemReview("rank_consistency", "required", "Compare coefficient rank and augmented rank."),
        AdvancedLinearSystemReview("feasibility_review", "required", "Review nonnegativity, capacity, legal, ethical, and operational constraints."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_linear_system_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_linear_system_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Linear System Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_linear_system_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced linear system review complete.")


if __name__ == "__main__":
    main()
