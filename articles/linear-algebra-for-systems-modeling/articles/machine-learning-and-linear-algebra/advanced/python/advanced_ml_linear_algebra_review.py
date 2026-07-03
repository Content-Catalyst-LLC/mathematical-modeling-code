from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedMLLinearAlgebraReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedMLLinearAlgebraReview]:
    return [
        AdvancedMLLinearAlgebraReview("feature_matrix", "required", "Define observations, features, units, preprocessing, missing-data handling, and matrix shape."),
        AdvancedMLLinearAlgebraReview("label_definition", "required", "Document label construction, proxy risks, target validity, and measurement provenance."),
        AdvancedMLLinearAlgebraReview("conditioning", "required", "Report feature scaling, rank, singular values, Gram conditioning, and numerical stability."),
        AdvancedMLLinearAlgebraReview("model_class", "required", "State model family, parameter structure, loss function, and approximation assumptions."),
        AdvancedMLLinearAlgebraReview("regularization", "required", "Document penalty type, strength, validation method, and effect on weights or rank."),
        AdvancedMLLinearAlgebraReview("validation_design", "required", "Report train-test split, cross-validation, time split, residual review, and relevant metrics."),
        AdvancedMLLinearAlgebraReview("distribution_shift", "required", "Review whether deployment data may differ from training and validation data."),
        AdvancedMLLinearAlgebraReview("responsible_interpretation", "required", "Interpret weights, components, embeddings, scores, and predictions as learned artifacts, not automatic causes or truths."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_ml_linear_algebra_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_ml_linear_algebra_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Machine Learning and Linear Algebra Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_ml_linear_algebra_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced machine learning linear algebra review complete.")


if __name__ == "__main__":
    main()
