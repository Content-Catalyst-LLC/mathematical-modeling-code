from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedLongRunReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedLongRunReview]:
    return [
        AdvancedLongRunReview("stationary_vs_limiting", "required", "Distinguish stationary distributions from actual limiting behavior."),
        AdvancedLongRunReview("initial_condition_sensitivity", "required", "Compare different starting distributions to test path dependence."),
        AdvancedLongRunReview("convergence_speed", "required", "Measure whether convergence occurs within a practical decision horizon."),
        AdvancedLongRunReview("closed_classes_absorption", "required", "Review absorbing states and closed classes for lock-in or terminal outcomes."),
        AdvancedLongRunReview("periodicity", "recommended", "Check whether cycles prevent simple convergence."),
        AdvancedLongRunReview("transition_rule_validity", "required", "Review whether a fixed transition matrix remains valid over repeated steps."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_long_run_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_long_run_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Long-Run Transition Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_long_run_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced long-run transition review complete.")


if __name__ == "__main__":
    main()
