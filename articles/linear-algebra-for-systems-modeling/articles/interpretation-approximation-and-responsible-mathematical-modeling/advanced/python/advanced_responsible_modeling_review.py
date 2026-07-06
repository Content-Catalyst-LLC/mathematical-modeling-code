from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedResponsibleModelingReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedResponsibleModelingReview]:
    return [
        AdvancedResponsibleModelingReview("model_purpose", "required", "State whether the model is exploratory, predictive, explanatory, diagnostic, optimization-oriented, or governance-supporting."),
        AdvancedResponsibleModelingReview("claim_type", "required", "Match claim strength to evidence strength and avoid overclaiming."),
        AdvancedResponsibleModelingReview("approximation_boundary", "required", "Document what the approximation preserves and what it loses."),
        AdvancedResponsibleModelingReview("uncertainty_sources", "required", "Separate data, model, numerical, sampling, and interpretive uncertainty."),
        AdvancedResponsibleModelingReview("validation_status", "required", "Preserve internal, data, model, predictive, interpretive, and use-case validation evidence."),
        AdvancedResponsibleModelingReview("diagnostic_evidence", "required", "Record residual diagnostics, condition checks, rank checks, and reconstruction error where relevant."),
        AdvancedResponsibleModelingReview("sensitivity_review", "required", "Compare conclusions across reasonable data, representation, scale, and model-form alternatives."),
        AdvancedResponsibleModelingReview("causal_caution", "required", "Separate prediction, association, explanation, mechanism, and causal interpretation."),
        AdvancedResponsibleModelingReview("accountability_path", "required", "Define who reviews, maintains, challenges, updates, and retires the model."),
        AdvancedResponsibleModelingReview("stop_use_conditions", "required", "Identify conditions where the model should not be used or should require additional review."),
        AdvancedResponsibleModelingReview("responsible_communication", "required", "Explain what the model shows, what it omits, how uncertain it is, and what it cannot justify."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_responsible_modeling_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_responsible_modeling_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Responsible Modeling Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_responsible_modeling_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced responsible modeling review complete.")


if __name__ == "__main__":
    main()
