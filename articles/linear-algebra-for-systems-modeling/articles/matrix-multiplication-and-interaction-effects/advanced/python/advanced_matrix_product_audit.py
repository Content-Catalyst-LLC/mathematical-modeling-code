from __future__ import annotations
import argparse, csv, json
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class AdvancedMatrixProductReview:
    review_item: str
    status: str
    governance_note: str

def build_reviews() -> list[AdvancedMatrixProductReview]:
    return [
        AdvancedMatrixProductReview("dimension_compatibility", "required", "Check inner dimensions and intermediate-layer meaning."),
        AdvancedMatrixProductReview("composition_order", "required", "Document what acts first and what acts second."),
        AdvancedMatrixProductReview("row_column_interpretation", "required", "Explain product entries as dot products or pathway aggregations."),
        AdvancedMatrixProductReview("unit_index_alignment", "required", "Review units, row/column order, and naming conventions."),
        AdvancedMatrixProductReview("noncommutativity_review", "required", "Do not reverse matrix order without a valid process interpretation."),
        AdvancedMatrixProductReview("indirect_effect_validation", "recommended", "Validate mediated pathways before treating product entries as effects."),
    ]

def write_outputs(output_dir: Path) -> None:
    rows = [asdict(review) for review in build_reviews()]
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    with (output_dir / "tables" / "advanced_matrix_product_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "advanced_matrix_product_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    report = ["# Advanced Matrix Product Review\n"] + [f"- **{row['review_item']}** ({row['status']}): {row['governance_note']}" for row in rows]
    (output_dir / "reports" / "advanced_matrix_product_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced matrix product review complete.")

if __name__ == "__main__":
    main()
