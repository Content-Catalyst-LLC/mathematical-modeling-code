from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedSimulationReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedSimulationReview]:
    return [
        AdvancedSimulationReview("state_vector", "required", "Define modeled variables, state dimension, units, resolution, and system boundary."),
        AdvancedSimulationReview("transition_rule", "required", "Document update equations, sparse structure, time step, external inputs, and stability diagnostics."),
        AdvancedSimulationReview("parameter_space", "required", "Document parameter ranges, baseline assumptions, stress scenarios, and intervention scenarios."),
        AdvancedSimulationReview("uncertainty_model", "required", "Document random input distributions, covariance assumptions, shock generation, and random seeds."),
        AdvancedSimulationReview("ensemble_design", "required", "Report ensemble size, time horizon, summary statistics, quantiles, extremes, and threshold exceedance."),
        AdvancedSimulationReview("dimensionality_management", "required", "Review sparsity, projections, reduced-order methods, compression, and information-loss diagnostics."),
        AdvancedSimulationReview("validation_design", "required", "Compare simulation behavior with observed data, known mechanisms, numerical checks, and domain review."),
        AdvancedSimulationReview("responsible_use", "required", "Present simulations as conditional model outcomes, not observations of the future or certainty."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_simulation_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_simulation_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Simulation of High-Dimensional Systems Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_simulation_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced high-dimensional simulation review complete.")


if __name__ == "__main__":
    main()
