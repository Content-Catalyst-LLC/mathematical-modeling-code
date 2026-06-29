from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path

Matrix = list[list[float]]
Vector = list[float]


@dataclass(frozen=True)
class LongRunTransitionAudit:
    system_name: str
    states: str
    orientation: str
    transition_matrix: str
    initial_distribution_a: str
    initial_distribution_b: str
    stationary_estimate: str
    distribution_a_after_25_steps: str
    distribution_b_after_25_steps: str
    convergence_distance_a: float
    convergence_distance_b: float
    initial_condition_gap_after_25_steps: float
    row_sum_error: float
    nonnegative: bool
    interpretation_warning: str


def matrix_to_string(A: Matrix) -> str:
    return ";".join(",".join(f"{value:.6f}" for value in row) for row in A)


def vector_to_string(v: Vector) -> str:
    return ",".join(f"{value:.6f}" for value in v)


def row_sum_error(P: Matrix) -> float:
    return max(abs(sum(row) - 1.0) for row in P)


def is_nonnegative(P: Matrix) -> bool:
    return all(value >= 0.0 for row in P for value in row)


def step(pi: Vector, P: Matrix) -> Vector:
    return [sum(pi[i] * P[i][j] for i in range(len(pi))) for j in range(len(P[0]))]


def evolve(pi: Vector, P: Matrix, steps: int) -> Vector:
    current = pi[:]
    for _ in range(steps):
        current = step(current, P)
    return current


def l1_distance(a: Vector, b: Vector) -> float:
    return sum(abs(x - y) for x, y in zip(a, b))


def normalize(v: Vector) -> Vector:
    total = sum(v)
    if abs(total) <= 1e-12:
        raise ValueError("cannot normalize vector with near-zero sum")
    return [x / total for x in v]


def stationary_by_iteration(P: Matrix, iterations: int = 1000) -> Vector:
    n = len(P)
    current = [1.0 / n] * n
    for _ in range(iterations):
        current = step(current, P)
    return normalize(current)


def build_audit() -> LongRunTransitionAudit:
    states = ["good", "fair", "poor"]

    P = [
        [0.82, 0.16, 0.02],
        [0.10, 0.76, 0.14],
        [0.03, 0.22, 0.75],
    ]

    initial_a = [0.80, 0.15, 0.05]
    initial_b = [0.10, 0.25, 0.65]

    stationary = stationary_by_iteration(P)
    a25 = evolve(initial_a, P, 25)
    b25 = evolve(initial_b, P, 25)

    return LongRunTransitionAudit(
        system_name="long_run_infrastructure_condition_transition_audit",
        states="|".join(states),
        orientation="row_stochastic_row_vector_update_pi_next_equals_pi_P",
        transition_matrix=matrix_to_string(P),
        initial_distribution_a=vector_to_string(initial_a),
        initial_distribution_b=vector_to_string(initial_b),
        stationary_estimate=vector_to_string(stationary),
        distribution_a_after_25_steps=vector_to_string(a25),
        distribution_b_after_25_steps=vector_to_string(b25),
        convergence_distance_a=round(l1_distance(a25, stationary), 12),
        convergence_distance_b=round(l1_distance(b25, stationary), 12),
        initial_condition_gap_after_25_steps=round(l1_distance(a25, b25), 12),
        row_sum_error=round(row_sum_error(P), 12),
        nonnegative=is_nonnegative(P),
        interpretation_warning=(
            "Long-run behavior depends on state definitions, transition orientation, time step, "
            "stationarity, convergence speed, absorbing or closed classes, and whether the fixed "
            "transition matrix remains valid over the modeled horizon."
        ),
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "long_run_transition_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "long_run_transition_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Long-run transition audit complete.")


if __name__ == "__main__":
    main()
