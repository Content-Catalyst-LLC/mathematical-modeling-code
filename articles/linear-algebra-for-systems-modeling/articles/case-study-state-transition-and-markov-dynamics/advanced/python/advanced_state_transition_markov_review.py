from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedStateTransitionMarkovReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedStateTransitionMarkovReview]:
    return [
        AdvancedStateTransitionMarkovReview("state_definition", "required", "Define whether states represent condition, risk, behavior, status, regime, location, health, compliance, or process stage."),
        AdvancedStateTransitionMarkovReview("transition_semantics", "required", "State whether transitions are observed frequencies, probabilities, policy rules, simulations, expert judgments, or scenario assumptions."),
        AdvancedStateTransitionMarkovReview("time_step", "required", "Document whether one step represents a day, week, month, year, event, decision cycle, or operational interval."),
        AdvancedStateTransitionMarkovReview("stochastic_check", "required", "Verify nonnegative probabilities, row or column sums, and matrix orientation."),
        AdvancedStateTransitionMarkovReview("markov_assumption", "required", "Review whether history, cumulative exposure, repeated disruption, policy intervention, or hidden subgroups affect transitions."),
        AdvancedStateTransitionMarkovReview("stationary_interpretation", "required", "Check convergence, reducibility, periodicity, spectral gap, and stability of transition probabilities."),
        AdvancedStateTransitionMarkovReview("absorption_review", "required", "Identify absorbing states and determine whether irreversibility is justified."),
        AdvancedStateTransitionMarkovReview("sensitivity_testing", "required", "Compare baseline, stress, intervention, time-varying, and uncertainty-perturbed transition matrices."),
        AdvancedStateTransitionMarkovReview("validation_status", "required", "Compare predicted state distributions with held-out observations, historical cases, simulation benchmarks, or domain expectations."),
        AdvancedStateTransitionMarkovReview("decision_boundary", "required", "Attach interpretation limits, uncertainty notes, validation status, and stop-use conditions to outputs."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_state_transition_markov_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_state_transition_markov_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced State Transition and Markov Dynamics Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_state_transition_markov_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced state transition and Markov dynamics review complete.")


if __name__ == "__main__":
    main()
