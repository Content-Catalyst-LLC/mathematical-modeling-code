from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedRankNullityReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedRankNullityReview]:
    return [
        AdvancedRankNullityReview("rank_interpretation", "required", "Interpret rank as independent structure, not model adequacy."),
        AdvancedRankNullityReview("nullity_interpretation", "required", "Interpret nullity as freedom, non-identifiability, or missing constraints."),
        AdvancedRankNullityReview("row_dependence_review", "required", "Review dependent rows as redundant or meaningful constraints."),
        AdvancedRankNullityReview("column_dependence_review", "required", "Review dependent columns as overlapping variables or features."),
        AdvancedRankNullityReview("rank_deficiency_review", "required", "Explain whether rank deficiency is expected, useful, or problematic."),
        AdvancedRankNullityReview("numerical_rank_tolerance", "required", "Document tolerance and test sensitivity of numerical rank decisions."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_rank_nullity_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_rank_nullity_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Rank-Nullity Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_rank_nullity_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced rank-nullity review complete.")


if __name__ == "__main__":
    main()
