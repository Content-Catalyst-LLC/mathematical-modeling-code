from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedGeometryReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedGeometryReview]:
    return [
        AdvancedGeometryReview("inner_product_definition", "required", "State whether geometry is Euclidean, weighted, covariance-aware, or domain-specific."),
        AdvancedGeometryReview("norm_choice", "required", "Document which norm measures residuals, error, distance, or convergence."),
        AdvancedGeometryReview("scaling_units", "required", "Check whether coordinate units make distance meaningful."),
        AdvancedGeometryReview("weights_review", "required", "Justify weights as risk, cost, uncertainty, reliability, priority, or energy."),
        AdvancedGeometryReview("covariance_review", "recommended", "Use covariance-aware distance only when covariance estimates are reliable."),
        AdvancedGeometryReview("translation_back", "recommended", "Translate normalized or weighted distances back into domain terms."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_state_space_geometry_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_state_space_geometry_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced State-Space Geometry Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_state_space_geometry_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced state-space geometry review complete.")


if __name__ == "__main__":
    main()
