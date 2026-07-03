from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedOrthogonalDecompositionReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedOrthogonalDecompositionReview]:
    return [
        AdvancedOrthogonalDecompositionReview("subspace_choice", "required", "Define what modeled directions are included and what is excluded."),
        AdvancedOrthogonalDecompositionReview("basis_construction", "required", "Document basis construction, orthogonalization method, scaling, and centering."),
        AdvancedOrthogonalDecompositionReview("projection_method", "required", "State whether projection, QR, SVD, normal equations, or iterative methods are used."),
        AdvancedOrthogonalDecompositionReview("rank_tolerance", "required", "Report algebraic rank, numerical rank, tolerance, and sensitivity to scaling."),
        AdvancedOrthogonalDecompositionReview("conditioning_review", "required", "Report condition number and numerical stability risks."),
        AdvancedOrthogonalDecompositionReview("residual_interpretation", "required", "Review whether residuals indicate noise, omitted structure, nonlinear effects, outliers, or boundary failure."),
        AdvancedOrthogonalDecompositionReview("validation_context", "required", "Connect approximation quality to the system question and downstream use."),
        AdvancedOrthogonalDecompositionReview("approximation_accountability", "recommended", "Review whose patterns, risks, or signals may be hidden by structured simplification."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_orthogonal_decomposition_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_orthogonal_decomposition_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Orthogonal Decomposition and Structured Approximation Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_orthogonal_decomposition_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced orthogonal decomposition review complete.")


if __name__ == "__main__":
    main()
