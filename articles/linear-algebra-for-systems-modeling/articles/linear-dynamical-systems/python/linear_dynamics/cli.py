from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

Matrix = list[list[float]]
Vector = list[float]


@dataclass(frozen=True)
class LinearDynamicsAudit:
    system_name: str
    state_names: str
    update_matrix: str
    initial_state: str
    horizon: int
    final_state: str
    initial_norm: float
    final_norm: float
    eigenvalue_1: float
    eigenvalue_2: float
    spectral_radius: float
    stability_classification: str
    trajectory_warning: str
    interpretation_warning: str


def matvec(A: Matrix, x: Vector) -> Vector:
    return [sum(A[i][j] * x[j] for j in range(len(x))) for i in range(len(A))]


def norm2(x: Vector) -> float:
    return math.sqrt(sum(value * value for value in x))


def matrix_to_string(A: Matrix) -> str:
    return ";".join(",".join(f"{value:.6f}" for value in row) for row in A)


def vector_to_string(x: Vector) -> str:
    return ",".join(f"{value:.6f}" for value in x)


def trace_2x2(A: Matrix) -> float:
    return A[0][0] + A[1][1]


def determinant_2x2(A: Matrix) -> float:
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]


def eigenvalues_2x2(A: Matrix) -> tuple[float, float]:
    trace = trace_2x2(A)
    determinant = determinant_2x2(A)
    discriminant = trace * trace - 4.0 * determinant
    if discriminant < 0:
        raise ValueError("This teaching routine handles real eigenvalues only.")
    root = math.sqrt(discriminant)
    return ((trace + root) / 2.0, (trace - root) / 2.0)


def classify_discrete(spectral_radius: float) -> str:
    if spectral_radius < 1.0:
        return "asymptotically_stable_discrete_time"
    if abs(spectral_radius - 1.0) <= 1e-10:
        return "boundary_or_marginal_discrete_time"
    return "unstable_discrete_time"


def simulate(A: Matrix, x0: Vector, horizon: int) -> list[Vector]:
    trajectory = [x0]
    current = x0
    for _ in range(horizon):
        current = matvec(A, current)
        trajectory.append(current)
    return trajectory


def write_trajectory(output_dir: Path, trajectory: list[Vector]) -> None:
    path = output_dir / "tables" / "linear_dynamics_trajectory.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["step", "infrastructure_stress", "service_delay", "state_norm"])
        writer.writeheader()
        for step, state in enumerate(trajectory):
            writer.writerow({
                "step": step,
                "infrastructure_stress": round(state[0], 12),
                "service_delay": round(state[1], 12),
                "state_norm": round(norm2(state), 12),
            })


def build_audit() -> tuple[LinearDynamicsAudit, list[Vector]]:
    state_names = ["infrastructure_stress", "service_delay"]
    A = [
        [0.82, 0.12],
        [0.18, 0.76],
    ]
    x0 = [10.0, 4.0]
    horizon = 20
    trajectory = simulate(A, x0, horizon)
    final_state = trajectory[-1]
    eigenvalues = eigenvalues_2x2(A)
    spectral_radius = max(abs(value) for value in eigenvalues)

    audit = LinearDynamicsAudit(
        system_name="two_state_linear_dynamics_audit",
        state_names="|".join(state_names),
        update_matrix=matrix_to_string(A),
        initial_state=vector_to_string(x0),
        horizon=horizon,
        final_state=vector_to_string(final_state),
        initial_norm=round(norm2(x0), 12),
        final_norm=round(norm2(final_state), 12),
        eigenvalue_1=round(eigenvalues[0], 12),
        eigenvalue_2=round(eigenvalues[1], 12),
        spectral_radius=round(spectral_radius, 12),
        stability_classification=classify_discrete(spectral_radius),
        trajectory_warning=(
            "A finite simulated trajectory shows behavior over the chosen horizon, "
            "not necessarily all possible long-run behavior."
        ),
        interpretation_warning=(
            "Linear dynamics depend on state definitions, units, scaling, time step, "
            "matrix validity, constraint checks, and whether linearity is structural or approximate."
        ),
    )
    return audit, trajectory


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit, trajectory = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "linear_dynamics_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "linear_dynamics_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    write_trajectory(output_dir, trajectory)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Linear dynamics audit complete.")


if __name__ == "__main__":
    main()
