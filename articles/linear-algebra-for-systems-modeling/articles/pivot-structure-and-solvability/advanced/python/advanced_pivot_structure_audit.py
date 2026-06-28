from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedPivotStructureReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedPivotStructureReview]:
    return [
        AdvancedPivotStructureReview("pivot_column_record", "required", "Record pivot columns and connect them to modeled variables."),
        AdvancedPivotStructureReview("free_variable_review", "required", "Interpret free variables as flexibility, missing constraints, or unobservable directions."),
        AdvancedPivotStructureReview("rank_comparison", "required", "Compare coefficient rank and augmented rank."),
        AdvancedPivotStructureReview("augmented_pivot_review", "required", "Review augmented-only pivots as contradictions or diagnostic conflicts."),
        AdvancedPivotStructureReview("column_space_reachability", "recommended", "Interpret solvability as target reachability under modeled relationships."),
        AdvancedPivotStructureReview("tolerance_sensitivity", "required", "Test whether pivot and rank decisions depend on numerical tolerance."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_pivot_structure_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_pivot_structure_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Pivot Structure Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_pivot_structure_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced pivot structure review complete.")


if __name__ == "__main__":
    main()
