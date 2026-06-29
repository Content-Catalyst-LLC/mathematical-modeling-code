from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path

Matrix = list[list[float]]
Vector = list[float]


@dataclass(frozen=True)
class MarkovAudit:
    system_name: str
    states: str
    orientation: str
    transition_matrix: str
    initial_distribution: str
    row_sum_error: float
    nonnegative: bool
    one_step_distribution: str
    ten_step_distribution: str
    steady_state_estimate: str
    conservation_error: float
    interpretation_warning: str


def matrix_to_string(A: Matrix) -> str:
    return ";".join(",".join(f"{value:.6f}" for value in row) for row in A)


def vector_to_string(v: Vector) -> str:
    return ",".join(f"{value:.6f}" for value in v)


def row_sum_error(P: Matrix) -> float:
    return max(abs(sum(row) - 1.0) for row in P)


def is_nonnegative(P: Matrix) -> bool:
    return all(value >= 0.0 for row in P for value in row)


def row_vector_matrix_multiply(pi: Vector, P: Matrix) -> Vector:
    return [sum(pi[i] * P[i][j] for i in range(len(pi))) for j in range(len(P[0]))]


def evolve(pi: Vector, P: Matrix, steps: int) -> Vector:
    current = pi[:]
    for _ in range(steps):
        current = row_vector_matrix_multiply(current, P)
    return current


def normalize(v: Vector) -> Vector:
    total = sum(v)
    if abs(total) <= 1e-12:
        raise ValueError("cannot normalize vector with near-zero sum")
    return [x / total for x in v]


def build_audit() -> MarkovAudit:
    states = ["good", "fair", "poor"]
    P = [
        [0.82, 0.16, 0.02],
        [0.10, 0.76, 0.14],
        [0.03, 0.22, 0.75],
    ]
    pi0 = [0.60, 0.30, 0.10]
    pi1 = evolve(pi0, P, 1)
    pi10 = evolve(pi0, P, 10)

    steady = [1.0 / len(states)] * len(states)
    for _ in range(500):
        steady = evolve(steady, P, 1)
    steady = normalize(steady)

    conservation_error = abs(sum(pi10) - 1.0)

    return MarkovAudit(
        system_name="infrastructure_condition_transition_audit",
        states="|".join(states),
        orientation="row_stochastic_row_vector_update_pi_next_equals_pi_P",
        transition_matrix=matrix_to_string(P),
        initial_distribution=vector_to_string(pi0),
        row_sum_error=round(row_sum_error(P), 12),
        nonnegative=is_nonnegative(P),
        one_step_distribution=vector_to_string(pi1),
        ten_step_distribution=vector_to_string(pi10),
        steady_state_estimate=vector_to_string(steady),
        conservation_error=round(conservation_error, 12),
        interpretation_warning=(
            "Transition matrices depend on state definitions, time step, data quality, stationarity, "
            "and the Markov assumption. A steady state is a model-implied fixed distribution, "
            "not automatically a desirable system outcome."
        ),
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "markov_transition_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "markov_transition_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Markov transition matrix audit complete.")


if __name__ == "__main__":
    main()
