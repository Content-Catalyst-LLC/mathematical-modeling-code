from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedChangeOfBasisReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedChangeOfBasisReview]:
    return [
        AdvancedChangeOfBasisReview("basis_meaning", "required", "Document what each basis direction means in the modeled system."),
        AdvancedChangeOfBasisReview("rank_validation", "required", "Check that the basis matrix is full rank."),
        AdvancedChangeOfBasisReview("coordinate_recovery", "required", "Compute basis coordinates and reconstruction error."),
        AdvancedChangeOfBasisReview("similarity_review", "required", "Separate invariant structure from coordinate-specific entries."),
        AdvancedChangeOfBasisReview("conditioning_review", "required", "Assess whether the basis is numerically fragile."),
        AdvancedChangeOfBasisReview("translation_back", "recommended", "Explain transformed results in original system terms."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_change_of_basis_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_change_of_basis_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Change-of-Basis Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_change_of_basis_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced change-of-basis review complete.")


if __name__ == "__main__":
    main()
