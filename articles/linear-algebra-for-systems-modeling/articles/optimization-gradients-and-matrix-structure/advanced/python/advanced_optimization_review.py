from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedOptimizationReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedOptimizationReview]:
    return [
        AdvancedOptimizationReview("decision_variables", "required", "Define controllable variables, units, bounds, and relationship to real decision authority."),
        AdvancedOptimizationReview("objective_function", "required", "Document what is minimized or maximized and whether the objective is a valid proxy for the system goal."),
        AdvancedOptimizationReview("constraint_matrix", "required", "Document equality, inequality, feasibility, capacity, safety, policy, and ethical constraints."),
        AdvancedOptimizationReview("gradient_formula", "required", "Report gradient expression, update rule, step size, and final gradient norm."),
        AdvancedOptimizationReview("curvature_diagnostics", "required", "Report Hessian structure, eigenvalue or singular-value review, convexity, and conditioning."),
        AdvancedOptimizationReview("solver_convergence", "required", "Document solver method, stopping rules, objective history, and convergence status."),
        AdvancedOptimizationReview("sensitivity_testing", "required", "Test objective weights, constraints, data perturbations, regularization strength, and parameter uncertainty."),
        AdvancedOptimizationReview("responsible_use", "required", "Present the optimum as a model result under assumptions, not automatic policy, causality, or truth."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_optimization_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_optimization_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Optimization, Gradients, and Matrix Structure Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_optimization_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced optimization review complete.")


if __name__ == "__main__":
    main()
