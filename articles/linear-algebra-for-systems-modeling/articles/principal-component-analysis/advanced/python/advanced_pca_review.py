from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedPCAReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedPCAReview]:
    return [
        AdvancedPCAReview("data_matrix_construction", "required", "Define observations, variables, entries, units, weights, and missing-data handling."),
        AdvancedPCAReview("centering", "required", "Document the baseline around which variation is measured."),
        AdvancedPCAReview("scaling", "required", "State whether PCA uses original units, standardization, normalization, or weights."),
        AdvancedPCAReview("explained_variance", "required", "Report component variance, cumulative variance, and retained-rank rationale."),
        AdvancedPCAReview("scores_and_loadings", "required", "Separate observation scores from variable loadings and document sign conventions."),
        AdvancedPCAReview("residual_review", "required", "Report reconstruction error and review observations or variables poorly represented by retained components."),
        AdvancedPCAReview("outlier_review", "recommended", "Review whether extreme observations are errors, rare cases, or important transitions."),
        AdvancedPCAReview("validation_context", "required", "Validate reduced representation against the specific systems question and downstream use."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_pca_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_pca_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Principal Component Analysis Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_pca_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced PCA review complete.")


if __name__ == "__main__":
    main()
