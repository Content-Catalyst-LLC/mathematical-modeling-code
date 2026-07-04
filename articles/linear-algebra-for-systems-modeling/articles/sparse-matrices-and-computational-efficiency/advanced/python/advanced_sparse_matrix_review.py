from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedSparseMatrixReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedSparseMatrixReview]:
    return [
        AdvancedSparseMatrixReview("matrix_shape", "required", "Report rows, columns, dimensional scale, nonzero count, and density."),
        AdvancedSparseMatrixReview("nonzero_structure", "required", "Inspect sparsity pattern, degree distribution, connected components, blocks, and bands."),
        AdvancedSparseMatrixReview("zero_interpretation", "required", "Distinguish true absence, unknown relationships, ignored relationships, thresholded values, and impossible links."),
        AdvancedSparseMatrixReview("storage_format", "required", "Document COO, CSR, CSC, DIA, BSR, graph, or matrix-free representation and why it matches the workflow."),
        AdvancedSparseMatrixReview("solver_choice", "required", "State direct sparse, iterative, Krylov, preconditioned, or matrix-free method and why it matches structure."),
        AdvancedSparseMatrixReview("fill_in_risk", "required", "Review ordering, symbolic factorization, and fill-in risk before relying on direct sparse solvers."),
        AdvancedSparseMatrixReview("thresholding_rule", "required", "Document thresholds that convert weak values to zeros and test sensitivity."),
        AdvancedSparseMatrixReview("responsible_use", "required", "Interpret sparse outputs through omissions, structure, diagnostics, validation, and model limits."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_sparse_matrix_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_sparse_matrix_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Sparse Matrices and Computational Efficiency Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_sparse_matrix_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced sparse matrix review complete.")


if __name__ == "__main__":
    main()
