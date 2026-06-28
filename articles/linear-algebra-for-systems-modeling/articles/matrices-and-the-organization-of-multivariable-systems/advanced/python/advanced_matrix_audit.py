from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedMatrixReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedMatrixReview]:
    return [
        AdvancedMatrixReview("matrix_role", "required", "Classify the matrix before interpreting operations."),
        AdvancedMatrixReview("row_column_metadata", "required", "Document row and column definitions, order, units, and indexing."),
        AdvancedMatrixReview("entry_semantics", "required", "State whether entries are measurements, coefficients, links, probabilities, flows, or estimates."),
        AdvancedMatrixReview("orientation_check", "required", "Confirm multiplication and transpose behavior match the intended system orientation."),
        AdvancedMatrixReview("zero_missingness", "required", "Distinguish absence, no effect, baseline, and missing values."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_matrix_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_matrix_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Matrix Representation Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_matrix_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced matrix review complete.")


if __name__ == "__main__":
    main()
