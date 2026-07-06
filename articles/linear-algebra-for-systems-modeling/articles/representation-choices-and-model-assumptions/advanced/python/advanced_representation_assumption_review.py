from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedRepresentationAssumptionReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedRepresentationAssumptionReview]:
    return [
        AdvancedRepresentationAssumptionReview("system_boundary", "required", "Document what is included, excluded, and outside the representational scope of the matrix."),
        AdvancedRepresentationAssumptionReview("row_column_meaning", "required", "Record substantive meaning of rows and columns before interpreting any computation."),
        AdvancedRepresentationAssumptionReview("value_and_zero_meaning", "required", "Clarify what entries and zeros mean, including missingness and thresholding rules."),
        AdvancedRepresentationAssumptionReview("scale_and_units", "required", "Document raw units, standardization, normalization, transformations, and comparability assumptions."),
        AdvancedRepresentationAssumptionReview("encoding_and_aggregation", "required", "Review categorical encoding, aggregation, discretization, and resolution choices."),
        AdvancedRepresentationAssumptionReview("basis_and_coordinates", "required", "State whether interpretation occurs in original variables, standardized coordinates, PCA components, eigenmodes, or embeddings."),
        AdvancedRepresentationAssumptionReview("representation_sensitivity", "required", "Compare conclusions across alternative reasonable representations where conclusions matter."),
        AdvancedRepresentationAssumptionReview("responsible_interpretation", "required", "Communicate what the representation can support and what it cannot justify."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_representation_assumption_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_representation_assumption_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Representation Assumption Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_representation_assumption_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced representation assumption review complete.")


if __name__ == "__main__":
    main()
