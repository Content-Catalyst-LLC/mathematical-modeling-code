from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedLeastSquaresReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedLeastSquaresReview]:
    return [
        AdvancedLeastSquaresReview("shape_check", "required", "Document whether the system is overdetermined and why rows exceed unknowns."),
        AdvancedLeastSquaresReview("residual_review", "required", "Report residual vectors, residual norms, and residual patterns."),
        AdvancedLeastSquaresReview("rank_identifiability", "required", "Check full column rank and coefficient identifiability."),
        AdvancedLeastSquaresReview("solver_choice", "required", "Document normal equations, QR, SVD, or pseudoinverse workflow."),
        AdvancedLeastSquaresReview("conditioning_review", "required", "Assess scaling, condition estimates, and near dependence."),
        AdvancedLeastSquaresReview("criterion_review", "recommended", "Explain why squared-error minimization fits the modeling purpose."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_least_squares_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_least_squares_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Least-Squares Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_least_squares_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced least-squares review complete.")


if __name__ == "__main__":
    main()
