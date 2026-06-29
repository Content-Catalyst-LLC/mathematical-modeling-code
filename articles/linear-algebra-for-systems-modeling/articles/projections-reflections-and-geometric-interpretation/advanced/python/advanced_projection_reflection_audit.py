from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedGeometricReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedGeometricReview]:
    return [
        AdvancedGeometricReview("target_subspace", "required", "Document what the projection subspace means."),
        AdvancedGeometricReview("residual_interpretation", "required", "Explain whether residuals are noise, excluded structure, bias, or model limitation."),
        AdvancedGeometricReview("inner_product_choice", "required", "State which geometry defines distance and orthogonality."),
        AdvancedGeometricReview("projection_diagnostics", "required", "Check idempotence, symmetry, rank, and residual norm."),
        AdvancedGeometricReview("reflection_diagnostics", "required", "Check involution, length preservation, and orientation meaning."),
        AdvancedGeometricReview("numerical_stability", "recommended", "Avoid unstable normal-equation projection formulas when QR or SVD is better."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_geometric_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_geometric_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Projection and Reflection Review\n"] + [
        f"- **{review.review_item}** ({review.status}): {review.governance_note}"
        for review in reviews
    ]
    (output_dir / "reports" / "advanced_geometric_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced projection and reflection review complete.")


if __name__ == "__main__":
    main()
