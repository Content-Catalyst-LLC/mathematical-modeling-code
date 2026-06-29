from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedDiagonalizationReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedDiagonalizationReview]:
    return [
        AdvancedDiagonalizationReview("matrix_definition", "required", "Document what the matrix represents, including units, weights, and time step."),
        AdvancedDiagonalizationReview("eigenvector_basis", "required", "Confirm enough independent eigenvectors exist for full diagonalization."),
        AdvancedDiagonalizationReview("reconstruction_error", "required", "Report ||A - P D P^{-1}|| for computed diagonalization."),
        AdvancedDiagonalizationReview("condition_number_P", "required", "Estimate cond(P) before interpreting modal coordinates."),
        AdvancedDiagonalizationReview("modal_translation", "required", "Translate modal coordinates back into system-specific meaning."),
        AdvancedDiagonalizationReview("fallback_decomposition", "recommended", "Use Schur, SVD, or Jordan analysis when diagonalization is fragile or invalid."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_diagonalization_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_diagonalization_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Diagonalization and Decoupled Behavior Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_diagonalization_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced diagonalization review complete.")


if __name__ == "__main__":
    main()
