from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedMatrixComputationReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedMatrixComputationReview]:
    return [
        AdvancedMatrixComputationReview("matrix_shape", "required", "Report rows, columns, state dimension, feature dimension, constraint count, and operation scale."),
        AdvancedMatrixComputationReview("storage_format", "required", "Document dense, sparse, block, distributed, streamed, or matrix-free representation."),
        AdvancedMatrixComputationReview("sparsity_pattern", "required", "Report nonzero count, density, locality, block structure, and whether zeros have system meaning."),
        AdvancedMatrixComputationReview("solver_choice", "required", "State direct, iterative, randomized, low-rank, or matrix-free method and why it matches the problem."),
        AdvancedMatrixComputationReview("convergence_diagnostics", "required", "Report residual norms, tolerances, iteration count, and stopping rules."),
        AdvancedMatrixComputationReview("conditioning_precision", "required", "Review conditioning, scaling, numerical precision, roundoff risk, and stability."),
        AdvancedMatrixComputationReview("approximation_method", "required", "Document randomized sketches, truncated decompositions, sampling, compression, and approximation error."),
        AdvancedMatrixComputationReview("responsible_use", "required", "Interpret large-scale outputs through assumptions, diagnostics, validation, and model limits."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    rows = [asdict(review) for review in build_reviews()]

    with (output_dir / "tables" / "advanced_matrix_computation_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_matrix_computation_review.json").write_text(
        json.dumps(rows, indent=2, sort_keys=True),
        encoding="utf-8"
    )

    report = ["# Advanced Large-Scale Matrix Computation Review\n"]
    for row in rows:
        report.append(f"- **{row['review_item']}** ({row['status']}): {row['governance_note']}")
    (output_dir / "reports" / "advanced_matrix_computation_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced large-scale matrix computation review complete.")


if __name__ == "__main__":
    main()
