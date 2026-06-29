from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedMarkovReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedMarkovReview]:
    return [
        AdvancedMarkovReview("state_definitions", "required", "Define states clearly and review whether the state space is complete enough."),
        AdvancedMarkovReview("transition_orientation", "required", "Document row-stochastic or column-stochastic convention and update rule."),
        AdvancedMarkovReview("time_step", "required", "State the transition interval and avoid reusing probabilities across incompatible time scales."),
        AdvancedMarkovReview("stochastic_validation", "required", "Check nonnegativity and row or column sums before downstream analysis."),
        AdvancedMarkovReview("stationarity", "recommended", "Review whether transition probabilities remain valid over the modeled horizon."),
        AdvancedMarkovReview("long_run_interpretation", "required", "Interpret steady states as model-implied distributions, not automatic value claims."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_markov_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_markov_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Markov Transition Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_markov_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced Markov review complete.")


if __name__ == "__main__":
    main()
