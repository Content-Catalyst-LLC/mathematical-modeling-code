from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedDecompositionWorkflowReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedDecompositionWorkflowReview]:
    return [
        AdvancedDecompositionWorkflowReview("matrix_structure", "required", "Review shape, symmetry, sparsity, rank, scaling, definiteness, conditioning, and data source before factorization."),
        AdvancedDecompositionWorkflowReview("decomposition_choice", "required", "Match LU, QR, Cholesky, eigen, Schur, SVD, sparse, or low-rank workflow to task and matrix structure."),
        AdvancedDecompositionWorkflowReview("pivoting_and_ordering", "required", "Document row and column permutations used for stability, sparsity preservation, or fill-in reduction."),
        AdvancedDecompositionWorkflowReview("rank_tolerance", "required", "State tolerance used for rank estimates, pseudoinverses, and low-rank approximation."),
        AdvancedDecompositionWorkflowReview("reconstruction_error", "required", "Report factorization reconstruction error, approximation error, and solve residuals where relevant."),
        AdvancedDecompositionWorkflowReview("conditioning", "required", "Report condition estimates or singular spectra for sensitive computations."),
        AdvancedDecompositionWorkflowReview("component_interpretation", "required", "Interpret factors, modes, and components through domain review rather than treating them as automatic causes."),
        AdvancedDecompositionWorkflowReview("responsible_use", "required", "Communicate factorization limits, approximation loss, diagnostics, and assumption boundaries."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_decomposition_workflow_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_decomposition_workflow_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Decomposition Workflow Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_decomposition_workflow_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced decomposition workflow review complete.")


if __name__ == "__main__":
    main()
