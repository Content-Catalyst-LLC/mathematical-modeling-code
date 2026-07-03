from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedLeontiefReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedLeontiefReview]:
    return [
        AdvancedLeontiefReview("technical_coefficients", "required", "Document coefficient construction, sector orientation, imports, and fixed-coefficient assumptions."),
        AdvancedLeontiefReview("net_requirements", "required", "Check I minus A for invertibility, conditioning, and numerical stability."),
        AdvancedLeontiefReview("productivity_condition", "required", "Report spectral radius, feasibility, and nonnegative output checks."),
        AdvancedLeontiefReview("leontief_inverse", "required", "Export total requirements, direct and indirect dependence, and multiplier structure."),
        AdvancedLeontiefReview("shock_scenario", "required", "Define final demand shock and interpret under fixed-coefficient assumptions."),
        AdvancedLeontiefReview("extension_coefficients", "required", "Document environmental or social extension coefficients, units, allocation, and provenance."),
        AdvancedLeontiefReview("sensitivity_testing", "required", "Test coefficient perturbations, demand uncertainty, aggregation, and boundary choices."),
        AdvancedLeontiefReview("responsible_use", "required", "Present Leontief results as structured estimates, not automatic causal proof or complete forecasts."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_leontief_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_leontief_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Leontief Systems and Intersectoral Dependence Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_leontief_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced Leontief review complete.")


if __name__ == "__main__":
    main()
