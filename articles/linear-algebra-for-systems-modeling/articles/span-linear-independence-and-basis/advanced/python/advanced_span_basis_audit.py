from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedSpanBasisReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedSpanBasisReview]:
    return [
        AdvancedSpanBasisReview("span_claim", "required", "Define what vectors are claimed to generate and what remains outside their span."),
        AdvancedSpanBasisReview("coefficient_meaning", "required", "Record whether coefficients are weights, proportions, intensities, coordinates, or abstract parameters."),
        AdvancedSpanBasisReview("independence_claim", "required", "Distinguish mathematical independence from substantive or causal independence."),
        AdvancedSpanBasisReview("basis_choice", "required", "Document the basis, coordinate meanings, and interpretive cost of transformed bases."),
        AdvancedSpanBasisReview("rank_tolerance", "required", "Record numerical tolerance, scaling, and near-dependence warnings."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_span_basis_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_span_basis_review.json").write_text(
        json.dumps(rows, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    report = ["# Advanced Span, Independence, and Basis Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_span_basis_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced span and basis review complete.")


if __name__ == "__main__":
    main()
