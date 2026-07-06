from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedLinearityDistortionReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedLinearityDistortionReview]:
    return [
        AdvancedLinearityDistortionReview("linearity_assumption", "required", "Review additivity, proportionality, superposition, and coefficient stability."),
        AdvancedLinearityDistortionReview("local_vs_global_validity", "required", "State whether the linear model is local, global, exploratory, predictive, explanatory, or diagnostic."),
        AdvancedLinearityDistortionReview("residual_structure", "required", "Inspect residuals for curvature, thresholds, changing variance, subgroup differences, and time dependence."),
        AdvancedLinearityDistortionReview("interaction_review", "required", "Check whether variables modify each other's effects rather than contributing independently."),
        AdvancedLinearityDistortionReview("threshold_and_regime_review", "required", "Review saturation, capacity limits, discontinuities, and regime changes."),
        AdvancedLinearityDistortionReview("feedback_review", "required", "Assess whether outputs influence future inputs or whether the transition matrix changes with state."),
        AdvancedLinearityDistortionReview("aggregation_review", "required", "Determine whether averages hide subgroup, spatial, temporal, or network heterogeneity."),
        AdvancedLinearityDistortionReview("extrapolation_review", "required", "Flag predictions and scenarios outside observed or validated ranges."),
        AdvancedLinearityDistortionReview("causal_interpretation", "required", "Separate prediction, association, mechanism, and causal identification."),
        AdvancedLinearityDistortionReview("responsible_communication", "required", "Explain what the linear model clarifies, what it omits, and where distortion risk is highest."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_linearity_distortion_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_linearity_distortion_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Linearity Distortion Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_linearity_distortion_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced linearity distortion review complete.")


if __name__ == "__main__":
    main()
