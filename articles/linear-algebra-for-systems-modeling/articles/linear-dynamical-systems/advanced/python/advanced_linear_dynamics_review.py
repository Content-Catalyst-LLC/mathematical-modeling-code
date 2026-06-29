from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedLinearDynamicsReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedLinearDynamicsReview]:
    return [
        AdvancedLinearDynamicsReview("state_definition", "required", "Define state variables, units, scaling, and interpretive boundaries."),
        AdvancedLinearDynamicsReview("matrix_source", "required", "Document how the update matrix was constructed, estimated, or assumed."),
        AdvancedLinearDynamicsReview("time_step", "required", "State the interval represented by each update and avoid incompatible reuse."),
        AdvancedLinearDynamicsReview("linearity_claim", "required", "Classify linearity as structural, local, empirical, or exploratory."),
        AdvancedLinearDynamicsReview("stability_diagnostics", "required", "Report eigenvalues, spectral radius, state norms, and trajectory behavior."),
        AdvancedLinearDynamicsReview("constraint_validity", "recommended", "Check whether simulated states remain physically or institutionally meaningful."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_linear_dynamics_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_linear_dynamics_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Linear Dynamics Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_linear_dynamics_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced linear dynamics review complete.")


if __name__ == "__main__":
    main()
