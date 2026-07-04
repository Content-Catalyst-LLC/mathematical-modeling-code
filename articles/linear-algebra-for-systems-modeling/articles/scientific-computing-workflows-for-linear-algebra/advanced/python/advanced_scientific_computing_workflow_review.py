from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedScientificComputingWorkflowReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedScientificComputingWorkflowReview]:
    return [
        AdvancedScientificComputingWorkflowReview("matrix_construction", "required", "Document rows, columns, values, units, zeros, missingness, data source, and construction assumptions."),
        AdvancedScientificComputingWorkflowReview("representation_choice", "required", "Choose dense, sparse, structured, distributed, or matrix-free representation based on matrix structure and system scale."),
        AdvancedScientificComputingWorkflowReview("numerical_backend", "required", "Record BLAS, LAPACK, sparse libraries, package versions, hardware, threading, and language bindings."),
        AdvancedScientificComputingWorkflowReview("solver_configuration", "required", "Document solver, factorization, tolerance, precision, preconditioner, iteration count, and stopping reason."),
        AdvancedScientificComputingWorkflowReview("diagnostic_outputs", "required", "Save residuals, condition estimates, convergence histories, reconstruction errors, rank checks, and performance diagnostics."),
        AdvancedScientificComputingWorkflowReview("reproducibility_controls", "required", "Preserve scripts, environments, package versions, random seeds, inputs, outputs, logs, and generated reports."),
        AdvancedScientificComputingWorkflowReview("validation_evidence", "required", "Use reference cases, edge cases, domain checks, perturbation tests, and observed comparisons."),
        AdvancedScientificComputingWorkflowReview("responsible_use", "required", "Communicate assumptions, uncertainty, numerical limits, performance constraints, and interpretation boundaries."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_scientific_computing_workflow_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_scientific_computing_workflow_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Scientific Computing Workflow Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_scientific_computing_workflow_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced scientific computing workflow review complete.")


if __name__ == "__main__":
    main()
