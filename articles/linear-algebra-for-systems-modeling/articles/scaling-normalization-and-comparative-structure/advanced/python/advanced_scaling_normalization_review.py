from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedScalingNormalizationReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedScalingNormalizationReview]:
    return [
        AdvancedScalingNormalizationReview("raw_units", "required", "Document original units and whether absolute magnitude is the intended comparison."),
        AdvancedScalingNormalizationReview("centering_standardization", "required", "Record centering, mean, standard deviation, and interpretation as relative deviation."),
        AdvancedScalingNormalizationReview("minmax_normalization", "required", "Document observed ranges, outlier sensitivity, and external comparability limits."),
        AdvancedScalingNormalizationReview("vector_normalization", "required", "Clarify when direction or profile is being compared rather than magnitude."),
        AdvancedScalingNormalizationReview("row_column_normalization", "required", "Track whether row totals, column magnitudes, or feature units are removed."),
        AdvancedScalingNormalizationReview("conditioning_scaling", "required", "Record diagonal scaling, preconditioning, condition proxies, and back-transformation needs."),
        AdvancedScalingNormalizationReview("metric_choice", "required", "Document whether comparison uses Euclidean distance, cosine similarity, correlation, dot product, or another metric."),
        AdvancedScalingNormalizationReview("scale_sensitivity", "required", "Compare conclusions across raw, centered, standardized, normalized, and domain-scaled representations."),
        AdvancedScalingNormalizationReview("responsible_interpretation", "required", "Communicate whether outputs represent magnitude, deviation, proportion, direction, probability, or numerical balance."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_scaling_normalization_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_scaling_normalization_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Scaling and Normalization Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_scaling_normalization_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced scaling and normalization review complete.")


if __name__ == "__main__":
    main()
