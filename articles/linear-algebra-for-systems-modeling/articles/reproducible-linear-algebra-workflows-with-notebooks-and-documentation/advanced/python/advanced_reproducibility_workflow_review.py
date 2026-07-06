from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedReproducibilityWorkflowReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedReproducibilityWorkflowReview]:
    return [
        AdvancedReproducibilityWorkflowReview("matrix_construction", "required", "Document how source data become matrices and vectors, including rows, columns, values, units, zeros, missingness, and transformations."),
        AdvancedReproducibilityWorkflowReview("notebook_execution", "required", "Run notebooks from a clean state and prevent hidden state, stale outputs, and ambiguous execution order."),
        AdvancedReproducibilityWorkflowReview("environment_control", "required", "Record language versions, packages, numerical backends, runtime settings, hardware notes, and seeds."),
        AdvancedReproducibilityWorkflowReview("randomness_control", "required", "Document seeds, generators, sampling methods, randomized algorithms, and nondeterminism warnings."),
        AdvancedReproducibilityWorkflowReview("validation_tests", "required", "Include reference cases, residual checks, edge cases, domain checks, and diagnostic thresholds."),
        AdvancedReproducibilityWorkflowReview("generated_outputs", "required", "Generate tables, figures, reports, JSON files, manifests, and logs directly from workflow code."),
        AdvancedReproducibilityWorkflowReview("version_control", "required", "Use commits, changelogs, manifests, and output records to support audit trails and rollback."),
        AdvancedReproducibilityWorkflowReview("responsible_interpretation", "required", "Pair reproducibility with assumptions, uncertainty, validation status, and interpretation boundaries."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_reproducibility_workflow_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_reproducibility_workflow_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Reproducibility Workflow Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_reproducibility_workflow_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced reproducibility workflow review complete.")


if __name__ == "__main__":
    main()
