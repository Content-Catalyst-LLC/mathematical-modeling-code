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
class LeastSquaresAudit:
    system_name: str
    row_count: int
    column_count: int
    overdetermined: bool
    rank: int
    solution: str
    fitted_values: str
    residuals: str
    residual_norm: float
    solver_method: str
    interpretation_warning: str


def transpose(A: Matrix) -> Matrix:
    return [list(row) for row in zip(*A)]


def matmul(A: Matrix, B: Matrix) -> Matrix:
    return [
        [sum(a * b for a, b in zip(row, col)) for col in zip(*B)]
        for row in A
    ]


def matvec(A: Matrix, x: Vector) -> Vector:
    return [sum(a * b for a, b in zip(row, x)) for row in A]


def solve_2x2(A: Matrix, b: Vector) -> Vector:
    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    if abs(det) <= 1e-12:
        raise ValueError("Normal-equation matrix is singular or ill-conditioned.")
    return [
        (b[0] * A[1][1] - A[0][1] * b[1]) / det,
        (A[0][0] * b[1] - b[0] * A[1][0]) / det,
    ]


def norm2(v: Vector) -> float:
    return math.sqrt(sum(value * value for value in v))


def build_audit() -> LeastSquaresAudit:
    A = [
        [1.0, 1.0],
        [1.0, 2.0],
        [1.0, 3.0],
        [1.0, 4.0],
    ]
    b = [2.0, 2.9, 4.1, 5.1]

    At = transpose(A)
    AtA = matmul(At, A)
    Atb = matvec(At, b)
    solution = solve_2x2(AtA, Atb)
    fitted = matvec(A, solution)
    residuals = [observed - fit for observed, fit in zip(b, fitted)]
    residual_norm = norm2(residuals)

    return LeastSquaresAudit(
        system_name="four_observation_linear_calibration",
        row_count=len(A),
        column_count=len(A[0]),
        overdetermined=len(A) > len(A[0]),
        rank=2,
        solution=",".join(f"{value:.6f}" for value in solution),
        fitted_values=",".join(f"{value:.6f}" for value in fitted),
        residuals=",".join(f"{value:.6f}" for value in residuals),
        residual_norm=round(residual_norm, 12),
        solver_method="normal equations for transparent teaching example; use QR or SVD for robust numerical workflows",
        interpretation_warning=(
            "Least squares minimizes squared residuals; fit quality, residual patterns, "
            "scaling, rank, conditioning, and model purpose still require review."
        ),
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "least_squares_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "least_squares_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Least squares audit complete.")


if __name__ == "__main__":
    main()
