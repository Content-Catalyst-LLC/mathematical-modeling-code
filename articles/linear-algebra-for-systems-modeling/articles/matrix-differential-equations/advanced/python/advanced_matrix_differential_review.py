from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedMatrixDifferentialReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedMatrixDifferentialReview]:
    return [
        AdvancedMatrixDifferentialReview("state_and_units", "required", "Define state variables, derivative units, and time units."),
        AdvancedMatrixDifferentialReview("continuous_time_interpretation", "required", "State explicitly that A is a continuous-time generator or rate matrix."),
        AdvancedMatrixDifferentialReview("matrix_source", "required", "Document whether the system matrix is physical, empirical, local Jacobian, or scenario-based."),
        AdvancedMatrixDifferentialReview("stability_diagnostics", "required", "Classify stability using eigenvalue real parts and inspect oscillatory modes."),
        AdvancedMatrixDifferentialReview("solver_reliability", "required", "Review numerical method, step size, stiffness, and matrix exponential computation."),
        AdvancedMatrixDifferentialReview("constraint_validity", "recommended", "Check whether simulated states remain physically or institutionally meaningful."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_matrix_differential_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_matrix_differential_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Matrix Differential Equation Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_matrix_differential_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced matrix differential equation review complete.")


if __name__ == "__main__":
    main()
