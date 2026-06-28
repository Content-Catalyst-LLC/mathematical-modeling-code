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
class InverseRecoveryAudit:
    system_name: str
    matrix_size: int
    determinant: float
    invertible: bool
    rank: int
    nullity: int
    recovered_solution: str
    residual_norm: float
    condition_warning: str
    tolerance: float
    interpretation_warning: str


def determinant_3x3(A: Matrix) -> float:
    return (
        A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
        - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
        + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0])
    )


def inverse_3x3(A: Matrix) -> Matrix:
    det = determinant_3x3(A)
    if abs(det) <= 1e-12:
        raise ValueError("Matrix is singular or effectively singular.")
    cofactors = [
        [A[1][1] * A[2][2] - A[1][2] * A[2][1], -(A[1][0] * A[2][2] - A[1][2] * A[2][0]), A[1][0] * A[2][1] - A[1][1] * A[2][0]],
        [-(A[0][1] * A[2][2] - A[0][2] * A[2][1]), A[0][0] * A[2][2] - A[0][2] * A[2][0], -(A[0][0] * A[2][1] - A[0][1] * A[2][0])],
        [A[0][1] * A[1][2] - A[0][2] * A[1][1], -(A[0][0] * A[1][2] - A[0][2] * A[1][0]), A[0][0] * A[1][1] - A[0][1] * A[1][0]],
    ]
    adjugate = [[cofactors[j][i] for j in range(3)] for i in range(3)]
    return [[value / det for value in row] for row in adjugate]


def matvec(A: Matrix, x: Vector) -> Vector:
    return [sum(a * b for a, b in zip(row, x)) for row in A]


def norm2(v: Vector) -> float:
    return math.sqrt(sum(x * x for x in v))


def build_audit() -> InverseRecoveryAudit:
    A = [[1.0, 1.0, 0.0], [0.0, 1.0, 1.0], [1.0, 0.0, 1.0]]
    b = [100.0, 80.0, 90.0]
    tolerance = 1e-10
    det_value = determinant_3x3(A)
    invertible = abs(det_value) > tolerance
    rank = 3 if invertible else 2
    nullity = len(A) - rank
    if invertible:
        recovered = matvec(inverse_3x3(A), b)
        residual = [lhs - rhs for lhs, rhs in zip(matvec(A, recovered), b)]
        residual_norm = norm2(residual)
    else:
        recovered = []
        residual_norm = float("nan")
    return InverseRecoveryAudit(
        system_name="three_constraint_structural_recovery_system",
        matrix_size=len(A),
        determinant=round(det_value, 10),
        invertible=invertible,
        rank=rank,
        nullity=nullity,
        recovered_solution=",".join(f"{value:.6f}" for value in recovered) if recovered else "not_available",
        residual_norm=round(residual_norm, 12) if invertible else residual_norm,
        condition_warning="inverse exists for this example; still review conditioning, units, and sensitivity" if invertible else "inverse does not exist; use rank, pseudoinverse, or least-squares diagnostics",
        tolerance=tolerance,
        interpretation_warning="Inverse recovery is algebraic; practical recovery requires review of conditioning, measurement error, units, constraints, and model meaning.",
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    audit = build_audit()
    row = asdict(audit)
    with (output_dir / "tables" / "inverse_recovery_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)
    (output_dir / "json" / "inverse_recovery_audit.json").write_text(json.dumps(row, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Inverse recovery audit complete.")


if __name__ == "__main__":
    main()
