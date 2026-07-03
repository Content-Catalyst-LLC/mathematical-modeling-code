from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedInputOutputReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedInputOutputReview]:
    return [
        AdvancedInputOutputReview("sector_classification", "required", "Define sector classification, aggregation level, region, year, and valuation basis."),
        AdvancedInputOutputReview("transactions_matrix", "required", "Document orientation, source, accounting framework, imports, and suppressed or estimated cells."),
        AdvancedInputOutputReview("technical_coefficients", "required", "Document coefficient construction, zero-output handling, and fixed-coefficient assumptions."),
        AdvancedInputOutputReview("leontief_system", "required", "Check invertibility, condition number, productivity assumptions, and solver diagnostics."),
        AdvancedInputOutputReview("multiplier_interpretation", "required", "Report multipliers as structured estimates under assumptions, not automatic causal proof."),
        AdvancedInputOutputReview("scenario_sensitivity", "required", "Test final demand shocks, coefficient uncertainty, and aggregation/boundary changes."),
        AdvancedInputOutputReview("environmental_extension", "required", "Document extension coefficients, units, allocation, provenance, and boundary assumptions."),
        AdvancedInputOutputReview("responsible_use", "required", "Connect results to uncertainty, limitations, domain context, and decision consequences."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_input_output_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_input_output_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Economic Input-Output Models Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_input_output_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced input-output review complete.")


if __name__ == "__main__":
    main()
