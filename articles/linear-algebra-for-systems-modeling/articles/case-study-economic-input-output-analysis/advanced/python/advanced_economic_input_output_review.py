from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedEconomicInputOutputReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedEconomicInputOutputReview]:
    return [
        AdvancedEconomicInputOutputReview("sector_definition", "required", "Document sector classification, aggregation level, geography, table year, and source."),
        AdvancedEconomicInputOutputReview("coefficient_construction", "required", "Record transaction sources, output denominators, price basis, domestic/import treatment, and matrix orientation."),
        AdvancedEconomicInputOutputReview("leontief_solution", "required", "Check invertibility, numerical stability, residuals, nonnegative outputs, and economic plausibility."),
        AdvancedEconomicInputOutputReview("condition_review", "required", "Estimate matrix conditioning and test sensitivity to coefficient perturbations."),
        AdvancedEconomicInputOutputReview("multiplier_interpretation", "required", "Define output, value-added, employment, emissions, or other multiplier type and avoid welfare overclaims."),
        AdvancedEconomicInputOutputReview("demand_scenario", "required", "Document scenario source, units, timing, price basis, affected sectors, and uncertainty."),
        AdvancedEconomicInputOutputReview("import_boundary", "required", "State whether coefficients are domestic, total, import-adjusted, regional, national, or multi-region."),
        AdvancedEconomicInputOutputReview("capacity_and_price_limits", "required", "State limits involving capacity constraints, price response, substitution, inventories, and behavioral adjustment."),
        AdvancedEconomicInputOutputReview("extension_factors", "required", "Document environmental or social extension sources, units, sector matching, and uncertainty."),
        AdvancedEconomicInputOutputReview("decision_boundary", "required", "Attach interpretation limits, validation status, uncertainty notes, and stop-use conditions to outputs."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_economic_input_output_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_economic_input_output_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Economic Input-Output Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_economic_input_output_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced economic input-output review complete.")


if __name__ == "__main__":
    main()
