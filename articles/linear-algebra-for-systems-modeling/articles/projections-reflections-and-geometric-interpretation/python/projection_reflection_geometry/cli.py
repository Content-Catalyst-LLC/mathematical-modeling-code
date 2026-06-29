from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

Vector = list[float]
Matrix = list[list[float]]


@dataclass(frozen=True)
class ProjectionReflectionAudit:
    system_name: str
    original_vector: str
    unit_direction: str
    projected_vector: str
    residual_vector: str
    residual_norm: float
    reflected_vector: str
    projection_idempotence_error: float
    projection_symmetry_error: float
    reflection_involution_error: float
    length_preservation_error: float
    interpretation_warning: str


def dot(a: Vector, b: Vector) -> float:
    return sum(x * y for x, y in zip(a, b))


def norm2(v: Vector) -> float:
    return math.sqrt(dot(v, v))


def matvec(A: Matrix, x: Vector) -> Vector:
    return [dot(row, x) for row in A]


def matmul(A: Matrix, B: Matrix) -> Matrix:
    return [[sum(a * b for a, b in zip(row, col)) for col in zip(*B)] for row in A]


def transpose(A: Matrix) -> Matrix:
    return [list(col) for col in zip(*A)]


def outer(u: Vector, v: Vector) -> Matrix:
    return [[a * b for b in v] for a in u]


def identity(n: int) -> Matrix:
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def matrix_subtract(A: Matrix, B: Matrix) -> Matrix:
    return [[a - b for a, b in zip(row_a, row_b)] for row_a, row_b in zip(A, B)]


def vector_subtract(a: Vector, b: Vector) -> Vector:
    return [x - y for x, y in zip(a, b)]


def matrix_norm(A: Matrix) -> float:
    return math.sqrt(sum(value * value for row in A for value in row))


def vector_to_string(v: Vector) -> str:
    return ",".join(f"{value:.6f}" for value in v)


def build_audit() -> ProjectionReflectionAudit:
    x = [4.0, 3.0]
    direction = [2.0, 1.0]
    u = [value / norm2(direction) for value in direction]

    P = outer(u, u)
    projected = matvec(P, x)
    residual = vector_subtract(x, projected)

    I = identity(2)
    R = [[2.0 * P[i][j] - I[i][j] for j in range(2)] for i in range(2)]
    reflected = matvec(R, x)

    return ProjectionReflectionAudit(
        system_name="two_dimensional_geometric_transformation_audit",
        original_vector=vector_to_string(x),
        unit_direction=vector_to_string(u),
        projected_vector=vector_to_string(projected),
        residual_vector=vector_to_string(residual),
        residual_norm=round(norm2(residual), 12),
        reflected_vector=vector_to_string(reflected),
        projection_idempotence_error=round(matrix_norm(matrix_subtract(matmul(P, P), P)), 12),
        projection_symmetry_error=round(matrix_norm(matrix_subtract(transpose(P), P)), 12),
        reflection_involution_error=round(matrix_norm(matrix_subtract(matmul(R, R), I)), 12),
        length_preservation_error=round(abs(norm2(reflected) - norm2(x)), 12),
        interpretation_warning=(
            "Projection retains the modeled direction and discards the perpendicular residual; "
            "reflection preserves distance while reversing the perpendicular component. "
            "Interpretation depends on the chosen geometry, units, scaling, and model purpose."
        ),
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "projection_reflection_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "projection_reflection_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Projection and reflection audit complete.")


if __name__ == "__main__":
    main()
