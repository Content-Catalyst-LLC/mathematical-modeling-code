from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedCrossLanguageMatrixReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedCrossLanguageMatrixReview]:
    return [
        AdvancedCrossLanguageMatrixReview("mathematical_intent", "required", "State the intended linear algebra operation before translating it into language-specific syntax."),
        AdvancedCrossLanguageMatrixReview("shape_discipline", "required", "Assert matrix and vector dimensions before and after products, solves, decompositions, and broadcasts."),
        AdvancedCrossLanguageMatrixReview("indexing_convention", "required", "Document zero-based, one-based, label-based, and query-order-dependent indexing when moving across languages."),
        AdvancedCrossLanguageMatrixReview("operator_semantics", "required", "Distinguish matrix multiplication, elementwise multiplication, dot products, and broadcasting for each language."),
        AdvancedCrossLanguageMatrixReview("storage_format", "required", "Document dense, sparse, tensor, data-frame, table, matrix-free, row-major, and column-major representations."),
        AdvancedCrossLanguageMatrixReview("numerical_diagnostics", "required", "Record residuals, condition numbers, rank, determinant, reconstruction error, and tolerances."),
        AdvancedCrossLanguageMatrixReview("interoperability", "required", "Preserve row IDs, column IDs, units, precision, missingness, schemas, and metadata across data exchange."),
        AdvancedCrossLanguageMatrixReview("responsible_use", "required", "Treat cross-language agreement as supporting evidence only when assumptions and diagnostics are documented."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_cross_language_matrix_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_cross_language_matrix_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Matrix Operations Across Modeling Languages Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_cross_language_matrix_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced cross-language matrix review complete.")


if __name__ == "__main__":
    main()
