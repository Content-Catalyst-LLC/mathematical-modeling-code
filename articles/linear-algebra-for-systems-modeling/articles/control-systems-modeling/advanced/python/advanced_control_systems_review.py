from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedControlReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedControlReview]:
    return [
        AdvancedControlReview("state_definition", "required", "Define state variables, units, scope, and what the controller is regulating."),
        AdvancedControlReview("input_authority", "required", "Document whether modeled inputs are physically, legally, institutionally, and ethically available."),
        AdvancedControlReview("output_reliability", "required", "Review measurement noise, bias, delay, and incomplete observation."),
        AdvancedControlReview("controllability_observability", "required", "Report ranks, conditioning, and unstable hidden or unreachable modes."),
        AdvancedControlReview("feedback_constraints", "required", "Check actuator saturation, state constraints, delays, rates, and input effort."),
        AdvancedControlReview("objective_governance", "required", "Document performance objectives, optimization weights, tradeoffs, and accountable decision authority."),
        AdvancedControlReview("robustness", "recommended", "Test perturbations to A, B, C, feedback gains, and initial conditions."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_control_systems_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_control_systems_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Control Systems Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_control_systems_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced control systems review complete.")


if __name__ == "__main__":
    main()
