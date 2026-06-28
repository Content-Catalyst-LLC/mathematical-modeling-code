from __future__ import annotations
import argparse, csv, json
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class Review:
    review_item: str
    status: str
    governance_note: str

def build_reviews() -> list[Review]:
    return [
        Review("square_matrix_check", "required", "Ordinary inverse claims require square matrices."),
        Review("invertibility_check", "required", "Record determinant, rank, pivots, and nullity before recovery claims."),
        Review("residual_check", "required", "Report residuals after recovered values are computed."),
        Review("conditioning_review", "required", "Assess whether recovery is numerically stable."),
        Review("solver_choice_review", "required", "Prefer solving systems directly over forming explicit inverses for numerical workflows."),
        Review("pseudoinverse_boundary", "recommended", "Use pseudoinverse language for rectangular, rank-deficient, or approximate recovery."),
    ]

def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(review) for review in build_reviews()]
    with (output_dir / "tables" / "advanced_inverse_recovery_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "advanced_inverse_recovery_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    report = ["# Advanced Inverse Recovery Review\n"] + [f"- **{row['review_item']}** ({row['status']}): {row['governance_note']}" for row in rows]
    (output_dir / "reports" / "advanced_inverse_recovery_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced inverse recovery review complete.")

if __name__ == "__main__":
    main()
