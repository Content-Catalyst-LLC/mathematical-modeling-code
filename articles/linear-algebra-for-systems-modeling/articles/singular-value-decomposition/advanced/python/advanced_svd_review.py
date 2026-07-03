from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedSVDReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedSVDReview]:
    return [
        AdvancedSVDReview("matrix_construction", "required", "Define rows, columns, entries, units, weights, missing data, and matrix meaning."),
        AdvancedSVDReview("preprocessing", "required", "Document centering, scaling, normalization, weighting, and missing-data handling."),
        AdvancedSVDReview("singular_spectrum", "required", "Report singular values, spectral gaps, rank tolerance, and numerical rank."),
        AdvancedSVDReview("conditioning_review", "required", "Report condition number and weak singular directions."),
        AdvancedSVDReview("pseudoinverse_threshold", "required", "Document which singular values are inverted, truncated, or regularized."),
        AdvancedSVDReview("retained_rank", "required", "Report retained rank, reconstruction error, explained energy, and validation performance."),
        AdvancedSVDReview("component_interpretation", "required", "Interpret singular vectors as mathematical directions, not automatic causes or categories."),
        AdvancedSVDReview("residual_review", "recommended", "Review discarded components for rare, local, or high-consequence structure."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_svd_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_svd_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Singular Value Decomposition Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_svd_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced SVD review complete.")


if __name__ == "__main__":
    main()
