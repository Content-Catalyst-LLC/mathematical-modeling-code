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
class ControlSystemsAudit:
    system_name: str
    state_names: str
    input_names: str
    output_names: str
    time_model: str
    state_matrix_A: str
    input_matrix_B: str
    output_matrix_C: str
    feedback_matrix_K: str
    open_loop_eigenvalues: str
    closed_loop_eigenvalues: str
    open_loop_max_real_part: float
    closed_loop_max_real_part: float
    controllability_rank: int
    observability_rank: int
    open_loop_final_state: str
    closed_loop_final_state: str
    max_control_effort: float
    control_warning: str
    interpretation_warning: str


def matrix_to_string(A: Matrix) -> str:
    return ";".join(",".join(f"{value:.6f}" for value in row) for row in A)


def vector_to_string(x: Vector) -> str:
    return ",".join(f"{value:.6f}" for value in x)


def matvec(A: Matrix, x: Vector) -> Vector:
    return [sum(A[i][j] * x[j] for j in range(len(x))) for i in range(len(A))]


def matmul(A: Matrix, B: Matrix) -> Matrix:
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def subtract(A: Matrix, B: Matrix) -> Matrix:
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def determinant_2x2(A: Matrix) -> float:
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]


def rank_2x2(A: Matrix, tolerance: float = 1e-10) -> int:
    if abs(determinant_2x2(A)) > tolerance:
        return 2
    if any(abs(value) > tolerance for row in A for value in row):
        return 1
    return 0


def eigenvalues_2x2_real(A: Matrix) -> tuple[float, float]:
    trace = A[0][0] + A[1][1]
    determinant = determinant_2x2(A)
    discriminant = trace * trace - 4.0 * determinant
    if discriminant < 0:
        raise ValueError("This teaching audit handles real eigenvalues only.")
    root = math.sqrt(discriminant)
    return ((trace + root) / 2.0, (trace - root) / 2.0)


def control_input(K: Matrix, x: Vector) -> Vector:
    raw = matvec(K, x)
    return [-value for value in raw]


def euler_open_loop(A: Matrix, x0: Vector, horizon: float, dt: float) -> Vector:
    x = x0[:]
    for _ in range(int(round(horizon / dt))):
        dx = matvec(A, x)
        x = [x[i] + dt * dx[i] for i in range(len(x))]
    return x


def euler_closed_loop(A: Matrix, B: Matrix, K: Matrix, x0: Vector, horizon: float, dt: float) -> tuple[Vector, float]:
    x = x0[:]
    max_effort = 0.0
    for _ in range(int(round(horizon / dt))):
        u = control_input(K, x)
        max_effort = max(max_effort, max(abs(value) for value in u))
        Ax = matvec(A, x)
        Bu = matvec(B, u)
        dx = [Ax[i] + Bu[i] for i in range(len(x))]
        x = [x[i] + dt * dx[i] for i in range(len(x))]
    return x, max_effort


def build_audit() -> ControlSystemsAudit:
    A = [[0.10, 1.00], [0.00, 0.20]]
    B = [[0.00], [1.00]]
    C = [[1.00, 0.00]]
    K = [[0.50, 1.40]]

    BK = matmul(B, K)
    A_closed = subtract(A, BK)

    open_eigs = eigenvalues_2x2_real(A)
    closed_eigs = eigenvalues_2x2_real(A_closed)

    AB = matmul(A, B)
    controllability = [[B[0][0], AB[0][0]], [B[1][0], AB[1][0]]]

    CA = matmul(C, A)
    observability = [[C[0][0], C[0][1]], [CA[0][0], CA[0][1]]]

    x0 = [3.0, 1.0]
    horizon = 8.0
    dt = 0.01

    open_final = euler_open_loop(A, x0, horizon, dt)
    closed_final, max_effort = euler_closed_loop(A, B, K, x0, horizon, dt)

    return ControlSystemsAudit(
        system_name="two_state_control_system_audit",
        state_names="position_like_state|velocity_like_state",
        input_names="single_control_input",
        output_names="measured_position_like_output",
        time_model="continuous_time_linear_state_space",
        state_matrix_A=matrix_to_string(A),
        input_matrix_B=matrix_to_string(B),
        output_matrix_C=matrix_to_string(C),
        feedback_matrix_K=matrix_to_string(K),
        open_loop_eigenvalues=vector_to_string(list(open_eigs)),
        closed_loop_eigenvalues=vector_to_string(list(closed_eigs)),
        open_loop_max_real_part=round(max(open_eigs), 12),
        closed_loop_max_real_part=round(max(closed_eigs), 12),
        controllability_rank=rank_2x2(controllability),
        observability_rank=rank_2x2(observability),
        open_loop_final_state=vector_to_string(open_final),
        closed_loop_final_state=vector_to_string(closed_final),
        max_control_effort=round(max_effort, 12),
        control_warning=(
            "The feedback law is evaluated without actuator saturation, delay, noise, "
            "or uncertainty. These must be reviewed before operational interpretation."
        ),
        interpretation_warning=(
            "Control models require state definition, input authority, output reliability, "
            "constraint checks, uncertainty review, objective transparency, and domain accountability."
        ),
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "control_systems_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "control_systems_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Control systems audit complete.")


if __name__ == "__main__":
    main()
