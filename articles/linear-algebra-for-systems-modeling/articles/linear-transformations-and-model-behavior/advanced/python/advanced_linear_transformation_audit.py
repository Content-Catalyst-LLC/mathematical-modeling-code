from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedTransformationReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedTransformationReview]:
    return [
        AdvancedTransformationReview("linearity_assumption", "required", "Document why addition and scalar multiplication are acceptable for the modeled context."),
        AdvancedTransformationReview("domain_codomain_review", "required", "Record input and output dimensions and meanings."),
        AdvancedTransformationReview("image_kernel_review", "required", "Document reachable outputs and invisible input directions."),
        AdvancedTransformationReview("basis_behavior_review", "required", "Interpret columns as transformed basis directions when meaningful."),
        AdvancedTransformationReview("rank_nullity_review", "required", "Connect rank and nullity to transformation behavior."),
        AdvancedTransformationReview("sensitivity_review", "recommended", "Assess amplification, damping, scaling, and conditioning before decision use."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_linear_transformation_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_linear_transformation_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Linear Transformation Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_linear_transformation_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced linear transformation review complete.")


if __name__ == "__main__":
    main()
