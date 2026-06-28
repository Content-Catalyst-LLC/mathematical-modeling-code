from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedMatrixArithmeticReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedMatrixArithmeticReview]:
    return [
        AdvancedMatrixArithmeticReview("shape_compatibility", "required", "Check formal matrix dimensions before entrywise arithmetic."),
        AdvancedMatrixArithmeticReview("semantic_alignment", "required", "Verify corresponding entries represent comparable system quantities."),
        AdvancedMatrixArithmeticReview("unit_scaling", "required", "Document units, normalization, and transformations before combining matrices."),
        AdvancedMatrixArithmeticReview("weight_meaning", "required", "Explain whether weights represent probability, priority, confidence, or sensitivity."),
        AdvancedMatrixArithmeticReview("component_traceability", "required", "Keep combined outputs traceable to source matrices and operations."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_matrix_arithmetic_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_matrix_arithmetic_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Matrix Arithmetic Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_matrix_arithmetic_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced matrix arithmetic review complete.")


if __name__ == "__main__":
    main()
