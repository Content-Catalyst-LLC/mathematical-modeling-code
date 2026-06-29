from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedEigenstructureReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedEigenstructureReview]:
    return [
        AdvancedEigenstructureReview("matrix_definition", "required", "Document what the matrix represents, including units, weights, and time step."),
        AdvancedEigenstructureReview("mode_interpretation", "required", "Explain what each major eigenvector mode means in domain terms."),
        AdvancedEigenstructureReview("spectral_radius_review", "required", "State how spectral radius is used for stability or amplification claims."),
        AdvancedEigenstructureReview("eigenpair_residuals", "required", "Report ||Av-lambda v|| for computed eigenpairs in production workflows."),
        AdvancedEigenstructureReview("spectral_gap", "recommended", "Review whether dominant modes are well separated."),
        AdvancedEigenstructureReview("nonnormality_conditioning", "recommended", "Check whether transient amplification or eigenvector sensitivity limits interpretation."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_eigenstructure_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_eigenstructure_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Eigenstructure and System Modes Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_eigenstructure_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced eigenstructure review complete.")


if __name__ == "__main__":
    main()
