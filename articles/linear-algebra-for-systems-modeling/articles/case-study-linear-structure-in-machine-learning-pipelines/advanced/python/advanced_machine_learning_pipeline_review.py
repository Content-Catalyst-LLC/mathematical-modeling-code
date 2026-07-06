from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedMachineLearningPipelineReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedMachineLearningPipelineReview]:
    return [
        AdvancedMachineLearningPipelineReview("observation_definition", "required", "Document sampling process, inclusion rules, time period, unit of analysis, missing records, and measurement context."),
        AdvancedMachineLearningPipelineReview("feature_definition", "required", "Record units, provenance, transformations, proxies, missingness, and known limitations."),
        AdvancedMachineLearningPipelineReview("target_definition", "required", "Document label source, timing, measurement process, subjectivity, delay, and relationship to the decision."),
        AdvancedMachineLearningPipelineReview("preprocessing", "required", "Document scaling, centering, imputation, encoding, normalization, projection, feature selection, and fitted parameters."),
        AdvancedMachineLearningPipelineReview("leakage_control", "required", "Fit preprocessing, feature selection, dimensionality reduction, model parameters, and thresholds inside training or validation workflows only."),
        AdvancedMachineLearningPipelineReview("baseline_model", "required", "Train transparent baselines and compare complex models against them using the same evaluation protocol."),
        AdvancedMachineLearningPipelineReview("evaluation", "required", "Report overall metrics, residuals, calibration, threshold sensitivity, subgroup error, rare-event performance, and temporal validation."),
        AdvancedMachineLearningPipelineReview("monitoring", "required", "Monitor feature drift, label shift, concept drift, embedding drift, residual drift, data pipeline changes, and retraining triggers."),
        AdvancedMachineLearningPipelineReview("interpretability_and_bias", "required", "Review coefficients, importances, embeddings, proxies, subgroup errors, and institutional context before making claims."),
        AdvancedMachineLearningPipelineReview("decision_boundary", "required", "Attach documentation, uncertainty, validation status, threshold rationale, oversight, appeals, and stop-use conditions to outputs."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_machine_learning_pipeline_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_machine_learning_pipeline_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Machine Learning Pipeline Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_machine_learning_pipeline_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced machine learning pipeline review complete.")


if __name__ == "__main__":
    main()
