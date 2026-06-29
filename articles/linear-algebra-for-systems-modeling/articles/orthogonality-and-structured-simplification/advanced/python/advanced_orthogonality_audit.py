from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedOrthogonalityReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedOrthogonalityReview]:
    return [
        AdvancedOrthogonalityReview("inner_product_definition", "required", "State the geometry defining orthogonality."),
        AdvancedOrthogonalityReview("scaling_units_review", "required", "Check whether units or normalization choices change dot-product meaning."),
        AdvancedOrthogonalityReview("tolerance_policy", "required", "Document numerical tolerance for near-zero dot products."),
        AdvancedOrthogonalityReview("residual_interpretation", "required", "Treat orthogonal residuals as substantive evidence, not automatic noise."),
        AdvancedOrthogonalityReview("orthogonality_error", "required", "Report ||Q^TQ-I|| or equivalent orthonormality diagnostic."),
        AdvancedOrthogonalityReview("solver_choice", "recommended", "Prefer QR or SVD over unstable normal-equation workflows when needed."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_orthogonality_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_orthogonality_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Orthogonality Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_orthogonality_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced orthogonality review complete.")


if __name__ == "__main__":
    main()
