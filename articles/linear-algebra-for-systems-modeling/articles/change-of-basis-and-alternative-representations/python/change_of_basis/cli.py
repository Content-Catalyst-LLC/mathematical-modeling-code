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
class ChangeOfBasisAudit:
    system_name: str
    basis_shape: str
    basis_rank: int
    basis_determinant: float
    basis_condition_warning: str
    original_vector: str
    basis_coordinates: str
    reconstructed_vector: str
    reconstruction_error: float
    transformed_matrix: str
    invariant_warning: str
    interpretation_warning: str


def matmul(A: Matrix, B: Matrix) -> Matrix:
    return [
        [sum(a * b for a, b in zip(row, col)) for col in zip(*B)]
        for row in A
    ]


def matvec(A: Matrix, x: Vector) -> Vector:
    return [sum(a * b for a, b in zip(row, x)) for row in A]


def det2(A: Matrix) -> float:
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]


def inv2(A: Matrix) -> Matrix:
    determinant = det2(A)
    if abs(determinant) <= 1e-12:
        raise ValueError("basis matrix is singular or numerically unsafe")
    return [
        [A[1][1] / determinant, -A[0][1] / determinant],
        [-A[1][0] / determinant, A[0][0] / determinant],
    ]


def norm2(v: Vector) -> float:
    return math.sqrt(sum(value * value for value in v))


def matrix_to_string(A: Matrix) -> str:
    return ";".join(",".join(f"{value:.6f}" for value in row) for row in A)


def vector_to_string(v: Vector) -> str:
    return ",".join(f"{value:.6f}" for value in v)


def build_audit() -> ChangeOfBasisAudit:
    P = [
        [2.0, 1.0],
        [1.0, 2.0],
    ]
    x = [5.0, 4.0]
    A = [
        [1.2, 0.3],
        [0.4, 0.9],
    ]

    Pinv = inv2(P)
    coords = matvec(Pinv, x)
    reconstructed = matvec(P, coords)
    reconstruction_error = norm2([a - b for a, b in zip(x, reconstructed)])
    transformed = matmul(matmul(Pinv, A), P)
    determinant = det2(P)
    basis_rank = 2 if abs(determinant) > 1e-12 else 1

    condition_warning = (
        "basis is valid in this teaching example; serious workflows should compute a numerical condition number"
        if abs(determinant) > 1e-8
        else "basis is near singular or unsafe for coordinate interpretation"
    )

    return ChangeOfBasisAudit(
        system_name="two_mode_representation_audit",
        basis_shape="2x2",
        basis_rank=basis_rank,
        basis_determinant=round(determinant, 12),
        basis_condition_warning=condition_warning,
        original_vector=vector_to_string(x),
        basis_coordinates=vector_to_string(coords),
        reconstructed_vector=vector_to_string(reconstructed),
        reconstruction_error=round(reconstruction_error, 12),
        transformed_matrix=matrix_to_string(transformed),
        invariant_warning=(
            "Similarity transformations preserve structural invariants such as determinant, trace, "
            "rank, and eigenvalues, but individual entries and interpretability change."
        ),
        interpretation_warning=(
            "Changing basis changes coordinate language; modelers must document basis meaning, "
            "units, scaling, conditioning, and how results translate back to system terms."
        ),
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "change_of_basis_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "change_of_basis_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Change-of-basis audit complete.")


if __name__ == "__main__":
    main()
