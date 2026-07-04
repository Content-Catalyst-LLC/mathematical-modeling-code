from __future__ import annotations

import argparse
import csv
import json
import math
import platform
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class ScientificComputingLinearAlgebraAudit:
    model_name: str
    workflow_stage: str
    matrix_shape: str
    representation: str
    precision: str
    solver_choice: str
    tolerance: float
    determinant: float
    condition_number_proxy: float
    matrix_vector_norm: float
    solution_norm: float
    residual_norm: float
    relative_residual: float
    reproducibility_status: str
    python_version: str
    platform_summary: str
    interpretation_warning: str


def matvec(A: list[list[float]], x: list[float]) -> list[float]:
    return [sum(row[j] * x[j] for j in range(len(x))) for row in A]


def norm2(x: list[float]) -> float:
    return math.sqrt(sum(v * v for v in x))


def det3(A: list[list[float]]) -> float:
    return (
        A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
        - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
        + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0])
    )


def solve3(A: list[list[float]], b: list[float]) -> list[float]:
    determinant = det3(A)
    if abs(determinant) < 1e-12:
        raise ValueError("Matrix is singular or too close to singular for this portable demonstration.")

    def replace_column(column_index: int) -> list[list[float]]:
        M = [row[:] for row in A]
        for row_index in range(3):
            M[row_index][column_index] = b[row_index]
        return M

    return [det3(replace_column(j)) / determinant for j in range(3)]


def transpose(A: list[list[float]]) -> list[list[float]]:
    return [list(col) for col in zip(*A)]


def frobenius_norm(A: list[list[float]]) -> float:
    return math.sqrt(sum(value * value for row in A for value in row))


def condition_proxy(A: list[list[float]]) -> float:
    inverse_columns = [solve3(A, e) for e in ([1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0])]
    inverse_matrix = transpose(inverse_columns)
    return frobenius_norm(A) * frobenius_norm(inverse_matrix)


def build_audit() -> ScientificComputingLinearAlgebraAudit:
    A = [
        [4.0, 1.0, 0.5],
        [1.0, 3.0, 0.25],
        [0.5, 0.25, 2.5],
    ]
    x_probe = [1.0, -1.0, 2.0]
    b = [6.0, 5.0, 2.0]
    tolerance = 1e-10

    y = matvec(A, x_probe)
    solution = solve3(A, b)
    residual = [bi - ai for bi, ai in zip(b, matvec(A, solution))]
    residual_norm = norm2(residual)
    relative_residual = residual_norm / max(norm2(b), 1e-15)
    status = "pass_residual_tolerance" if relative_residual <= tolerance else "review_required"

    return ScientificComputingLinearAlgebraAudit(
        model_name="scientific_computing_linear_algebra_audit",
        workflow_stage="matrix_construction_solve_diagnostics_metadata",
        matrix_shape="3x3",
        representation="dense_standard_library_demo_matrix",
        precision="double_precision_like_python_float",
        solver_choice="direct_small_system_solve_for_portable_demo",
        tolerance=tolerance,
        determinant=round(det3(A), 12),
        condition_number_proxy=round(condition_proxy(A), 12),
        matrix_vector_norm=round(norm2(y), 12),
        solution_norm=round(norm2(solution), 12),
        residual_norm=round(residual_norm, 12),
        relative_residual=round(relative_residual, 12),
        reproducibility_status=status,
        python_version=sys.version.split()[0],
        platform_summary=platform.platform(),
        interpretation_warning="Scientific computing outputs should be interpreted with matrix construction, precision, solver choice, tolerances, residuals, conditioning, environment metadata, validation checks, and model assumptions.",
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "scientific_computing_linear_algebra_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "scientific_computing_linear_algebra_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Scientific computing linear algebra audit complete.")


if __name__ == "__main__":
    main()
