from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedStabilityConditioningReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedStabilityConditioningReview]:
    return [
        AdvancedStabilityConditioningReview("floating_point_precision", "required", "Document precision, tolerance, equality tests, cancellation risk, and rounding assumptions."),
        AdvancedStabilityConditioningReview("conditioning", "required", "Report problem sensitivity using condition estimates and singular-value diagnostics where available."),
        AdvancedStabilityConditioningReview("condition_number", "required", "State norm choice or approximation method and interpret high values cautiously."),
        AdvancedStabilityConditioningReview("residual_norm", "required", "Report residual and relative residual for solves, least-squares fits, and iterative outputs."),
        AdvancedStabilityConditioningReview("solver_choice", "required", "Use solver methods matched to matrix structure, sparsity, rank, conditioning, and accuracy needs."),
        AdvancedStabilityConditioningReview("scaling", "required", "Document row, column, variable, unit, and feature scaling and connect outputs back to original units."),
        AdvancedStabilityConditioningReview("perturbation_testing", "required", "Assess output sensitivity under small input, coefficient, scenario, or tolerance changes."),
        AdvancedStabilityConditioningReview("responsible_use", "required", "Communicate numerical limits alongside uncertainty, assumptions, and model-purpose boundaries."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_stability_conditioning_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_stability_conditioning_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Numerical Stability and Conditioning Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_stability_conditioning_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced numerical stability and conditioning review complete.")


if __name__ == "__main__":
    main()
