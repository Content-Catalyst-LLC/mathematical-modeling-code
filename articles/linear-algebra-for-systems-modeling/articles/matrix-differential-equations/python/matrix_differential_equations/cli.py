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
class MatrixDifferentialAudit:
    system_name: str
    state_names: str
    system_matrix: str
    initial_state: str
    time_horizon: float
    eigenvalue_1: float
    eigenvalue_2: float
    max_real_part: float
    stability_classification: str
    final_state_estimate: str
    initial_norm: float
    final_norm: float
    time_model_warning: str
    interpretation_warning: str


def matrix_to_string(A: Matrix) -> str:
    return ";".join(",".join(f"{value:.6f}" for value in row) for row in A)


def vector_to_string(x: Vector) -> str:
    return ",".join(f"{value:.6f}" for value in x)


def norm2(x: Vector) -> float:
    return math.sqrt(sum(value * value for value in x))


def trace_2x2(A: Matrix) -> float:
    return A[0][0] + A[1][1]


def determinant_2x2(A: Matrix) -> float:
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]


def eigenvalues_2x2_real(A: Matrix) -> tuple[float, float]:
    trace = trace_2x2(A)
    determinant = determinant_2x2(A)
    discriminant = trace * trace - 4.0 * determinant
    if discriminant < 0:
        raise ValueError("This teaching routine handles real eigenvalues only.")
    root = math.sqrt(discriminant)
    return ((trace + root) / 2.0, (trace - root) / 2.0)


def classify_continuous(max_real_part: float) -> str:
    if max_real_part < 0.0:
        return "asymptotically_stable_continuous_time"
    if abs(max_real_part) <= 1e-10:
        return "boundary_or_marginal_continuous_time"
    return "unstable_continuous_time"


def matvec(A: Matrix, x: Vector) -> Vector:
    return [sum(A[i][j] * x[j] for j in range(len(x))) for i in range(len(A))]


def euler_simulate(A: Matrix, x0: Vector, horizon: float, dt: float) -> list[Vector]:
    steps = int(round(horizon / dt))
    trajectory = [x0[:]]
    x = x0[:]
    for _ in range(steps):
        dx = matvec(A, x)
        x = [x[i] + dt * dx[i] for i in range(len(x))]
        trajectory.append(x)
    return trajectory


def write_trajectory(output_dir: Path, trajectory: list[Vector], dt: float) -> None:
    path = output_dir / "tables" / "matrix_differential_equation_trajectory.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["time", "infrastructure_stress", "service_delay", "state_norm"])
        writer.writeheader()
        for step, state in enumerate(trajectory):
            writer.writerow({
                "time": round(step * dt, 8),
                "infrastructure_stress": round(state[0], 12),
                "service_delay": round(state[1], 12),
                "state_norm": round(norm2(state), 12),
            })


def build_audit() -> tuple[MatrixDifferentialAudit, list[Vector], float]:
    state_names = ["infrastructure_stress", "service_delay"]
    A = [
        [-0.28, 0.08],
        [0.12, -0.34],
    ]
    x0 = [10.0, 4.0]
    horizon = 10.0
    dt = 0.01
    eigenvalues = eigenvalues_2x2_real(A)
    max_real_part = max(eigenvalues)
    trajectory = euler_simulate(A, x0, horizon, dt)
    final_state = trajectory[-1]

    audit = MatrixDifferentialAudit(
        system_name="two_state_matrix_differential_equation_audit",
        state_names="|".join(state_names),
        system_matrix=matrix_to_string(A),
        initial_state=vector_to_string(x0),
        time_horizon=horizon,
        eigenvalue_1=round(eigenvalues[0], 12),
        eigenvalue_2=round(eigenvalues[1], 12),
        max_real_part=round(max_real_part, 12),
        stability_classification=classify_continuous(max_real_part),
        final_state_estimate=vector_to_string(final_state),
        initial_norm=round(norm2(x0), 12),
        final_norm=round(norm2(final_state), 12),
        time_model_warning=(
            "This matrix is interpreted as a continuous-time generator. "
            "Do not apply discrete-time spectral-radius rules to it."
        ),
        interpretation_warning=(
            "Matrix differential equations depend on state definitions, units, time scale, "
            "matrix source, linearity assumptions, solver choices, stiffness review, and domain constraints."
        ),
    )
    return audit, trajectory, dt


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit, trajectory, dt = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "matrix_differential_equation_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "matrix_differential_equation_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    write_trajectory(output_dir, trajectory, dt)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Matrix differential equation audit complete.")


if __name__ == "__main__":
    main()
