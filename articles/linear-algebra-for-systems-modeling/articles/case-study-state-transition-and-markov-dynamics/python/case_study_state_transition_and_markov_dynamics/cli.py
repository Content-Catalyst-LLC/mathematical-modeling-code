from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class StateTransitionMarkovAudit:
    workflow_name: str
    scenario_name: str
    state_count: int
    time_steps: int
    stochastic_check_passed: bool
    initial_primary_state: str
    highest_probability_state_after_horizon: str
    highest_probability_after_horizon: float
    stationary_highest_probability_state: str
    stationary_highest_probability: float
    stress_disrupted_probability_after_horizon: float
    baseline_disrupted_probability_after_horizon: float
    memoryless_warning: str
    interpretation_warning: str


STATES = ["normal", "strained", "disrupted", "recovered"]

TRANSITION_MATRIX = [
    [0.70, 0.20, 0.05, 0.05],
    [0.20, 0.50, 0.20, 0.10],
    [0.05, 0.25, 0.55, 0.15],
    [0.50, 0.20, 0.05, 0.25],
]

STRESS_TRANSITION_MATRIX = [
    [0.55, 0.30, 0.10, 0.05],
    [0.10, 0.45, 0.35, 0.10],
    [0.03, 0.17, 0.70, 0.10],
    [0.35, 0.30, 0.15, 0.20],
]


def row_stochastic(matrix: list[list[float]], tolerance: float = 1e-10) -> bool:
    return all(
        all(value >= -tolerance for value in row)
        and abs(sum(row) - 1.0) <= tolerance
        for row in matrix
    )


def transpose_matvec(matrix: list[list[float]], vector: list[float]) -> list[float]:
    n = len(vector)
    return [sum(matrix[i][j] * vector[i] for i in range(n)) for j in range(n)]


def evolve(matrix: list[list[float]], initial: list[float], steps: int) -> list[float]:
    state = initial[:]
    for _ in range(steps):
        state = transpose_matvec(matrix, state)
    total = sum(state)
    return [value / total for value in state]


def stationary_distribution(matrix: list[list[float]], iterations: int = 1000, tolerance: float = 1e-12) -> list[float]:
    n = len(matrix)
    state = [1.0 / n for _ in range(n)]
    for _ in range(iterations):
        nxt = transpose_matvec(matrix, state)
        if max(abs(nxt[i] - state[i]) for i in range(n)) < tolerance:
            state = nxt
            break
        state = nxt
    total = sum(state)
    return [value / total for value in state]


def build_audit() -> StateTransitionMarkovAudit:
    steps = 5
    initial = [1.0, 0.0, 0.0, 0.0]

    baseline = evolve(TRANSITION_MATRIX, initial, steps)
    stress = evolve(STRESS_TRANSITION_MATRIX, initial, steps)
    stationary = stationary_distribution(TRANSITION_MATRIX)

    highest_index = max(range(len(STATES)), key=lambda i: baseline[i])
    stationary_index = max(range(len(STATES)), key=lambda i: stationary[i])
    disrupted_index = STATES.index("disrupted")

    return StateTransitionMarkovAudit(
        workflow_name="state_transition_markov_audit",
        scenario_name="synthetic_infrastructure_condition_transition_model",
        state_count=len(STATES),
        time_steps=steps,
        stochastic_check_passed=row_stochastic(TRANSITION_MATRIX) and row_stochastic(STRESS_TRANSITION_MATRIX),
        initial_primary_state="normal",
        highest_probability_state_after_horizon=STATES[highest_index],
        highest_probability_after_horizon=round(baseline[highest_index], 12),
        stationary_highest_probability_state=STATES[stationary_index],
        stationary_highest_probability=round(stationary[stationary_index], 12),
        stress_disrupted_probability_after_horizon=round(stress[disrupted_index], 12),
        baseline_disrupted_probability_after_horizon=round(baseline[disrupted_index], 12),
        memoryless_warning="The Markov assumption treats the current state as sufficient for predicting the next state. If cumulative stress, repeated disruption, policy intervention, repair history, or hidden subgroups matter, the model should be expanded or treated as exploratory.",
        interpretation_warning="State transition results depend on state definitions, transition estimation, time-step choice, matrix orientation, sparse data, uncertainty, validation evidence, and scenario assumptions. Stationary distributions and multi-step probabilities describe the model, not guaranteed system destiny.",
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "state_transition_markov_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "state_transition_markov_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    report = [
        "# State Transition and Markov Dynamics Audit",
        "",
        f"- Workflow: {audit.workflow_name}",
        f"- Scenario: {audit.scenario_name}",
        f"- State count: {audit.state_count}",
        f"- Time steps: {audit.time_steps}",
        f"- Stochastic check passed: {audit.stochastic_check_passed}",
        f"- Initial primary state: {audit.initial_primary_state}",
        f"- Highest-probability state after horizon: {audit.highest_probability_state_after_horizon}",
        f"- Highest probability after horizon: {audit.highest_probability_after_horizon}",
        f"- Stationary highest-probability state: {audit.stationary_highest_probability_state}",
        f"- Stationary highest probability: {audit.stationary_highest_probability}",
        f"- Baseline disrupted probability after horizon: {audit.baseline_disrupted_probability_after_horizon}",
        f"- Stress disrupted probability after horizon: {audit.stress_disrupted_probability_after_horizon}",
        "",
        audit.memoryless_warning,
        "",
        audit.interpretation_warning,
    ]
    (output_dir / "reports" / "state_transition_markov_audit.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("State transition and Markov dynamics audit complete.")


if __name__ == "__main__":
    main()
