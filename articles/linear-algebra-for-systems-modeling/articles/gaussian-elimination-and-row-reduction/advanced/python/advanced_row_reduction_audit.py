from __future__ import annotations
import argparse, csv, json
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class AdvancedRowReductionReview:
    review_item: str
    status: str
    governance_note: str

def build_reviews() -> list[AdvancedRowReductionReview]:
    return [
        AdvancedRowReductionReview("original_matrix_documentation", "required", "Store the original augmented matrix before row operations."),
        AdvancedRowReductionReview("pivot_record", "required", "Record pivot columns, pivot choices, and tolerance."),
        AdvancedRowReductionReview("rank_consistency", "required", "Compare coefficient rank and augmented rank."),
        AdvancedRowReductionReview("free_variable_review", "required", "Interpret free variables as flexibility, missing constraints, or decision variables."),
        AdvancedRowReductionReview("solution_verification", "required", "Verify computed solutions against the original equations."),
        AdvancedRowReductionReview("numerical_stability", "required", "Review small pivots, scaling, conditioning, and false precision."),
    ]

def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(review) for review in build_reviews()]
    with (output_dir / "tables" / "advanced_row_reduction_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "advanced_row_reduction_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    report = ["# Advanced Row Reduction Review\n"] + [f"- **{row['review_item']}** ({row['status']}): {row['governance_note']}" for row in rows]
    (output_dir / "reports" / "advanced_row_reduction_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced row reduction review complete.")

if __name__ == "__main__":
    main()
