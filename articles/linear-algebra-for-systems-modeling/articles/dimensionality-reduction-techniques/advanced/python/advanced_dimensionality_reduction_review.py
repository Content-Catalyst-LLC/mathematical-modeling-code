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
        AdvancedDimensionalityReductionReview("original_matrix", "required", "Define observations, variables, entries, units, weights, and missing-data handling."),
        AdvancedDimensionalityReductionReview("preprocessing", "required", "Document centering, scaling, normalization, transformations, and weighting."),
        AdvancedDimensionalityReductionReview("reduction_method", "required", "State the method and what structure it is intended to preserve."),
        AdvancedDimensionalityReductionReview("target_dimension", "required", "Report reduced dimension, rank rationale, and sensitivity to dimension choice."),
        AdvancedDimensionalityReductionReview("information_loss", "required", "Report reconstruction error, residuals, distance distortion, or neighborhood preservation as appropriate."),
        AdvancedDimensionalityReductionReview("randomness_and_parameters", "required", "Document random seed, tolerances, solver settings, and method-specific parameters."),
        AdvancedDimensionalityReductionReview("validation_context", "required", "Validate reduced representation against the systems question and downstream use."),
        AdvancedDimensionalityReductionReview("responsible_interpretation", "required", "Treat reduced coordinates as model artifacts rather than causes, categories, or complete system truths."),
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

    report = ["# Advanced Dimensionality Reduction Techniques Review\n"]
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
