from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedDimensionalityReductionReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedDimensionalityReductionReview]:
    return [
        AdvancedDimensionalityReductionReview("observation_definition", "required", "Define what rows represent and what ethical or domain-specific stakes they carry."),
        AdvancedDimensionalityReductionReview("feature_definition", "required", "Record units, measurement sources, proxies, missingness, transformations, and feature provenance."),
        AdvancedDimensionalityReductionReview("preprocessing", "required", "Document centering, scaling, imputation, transformation, filtering, and outlier handling."),
        AdvancedDimensionalityReductionReview("leakage_control", "required", "Fit scaling and dimensionality reduction only on training folds or training data in predictive workflows."),
        AdvancedDimensionalityReductionReview("component_selection", "required", "Record explained variance, reconstruction error, stability evidence, downstream validation, and domain justification."),
        AdvancedDimensionalityReductionReview("reconstruction_review", "required", "Inspect total, per-feature, per-observation, subgroup, and task-specific reconstruction error."),
        AdvancedDimensionalityReductionReview("rare_pattern_preservation", "required", "Check whether rare, minority, local, or high-stakes structure is lost in reduction."),
        AdvancedDimensionalityReductionReview("stability_review", "required", "Test component and downstream stability across samples, perturbations, time windows, and feature sets."),
        AdvancedDimensionalityReductionReview("interpretability_review", "required", "Review loadings, component labels, visual clusters, and domain evidence before naming dimensions."),
        AdvancedDimensionalityReductionReview("decision_boundary", "required", "Attach preprocessing choices, component count, uncertainty notes, validation status, and stop-use conditions to outputs."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_dimensionality_reduction_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_dimensionality_reduction_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Dimensionality Reduction Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_dimensionality_reduction_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced dimensionality reduction review complete.")


if __name__ == "__main__":
    main()
