from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path

Matrix = list[list[float]]


@dataclass(frozen=True)
class MatrixArithmeticAudit:
    operation_name: str
    matrix_shape: str
    row_meaning: str
    column_meaning: str
    units: str
    weights: str
    compatible_shape: bool
    output_entry_sum: float
    interpretation_warning: str


def shape(matrix: Matrix) -> tuple[int, int]:
    return (len(matrix), len(matrix[0]) if matrix else 0)


def same_shape(*matrices: Matrix) -> bool:
    if not matrices:
        return False
    first_shape = shape(matrices[0])
    return all(shape(matrix) == first_shape for matrix in matrices)


def add(A: Matrix, B: Matrix) -> Matrix:
    if not same_shape(A, B):
        raise ValueError("Matrices must have the same shape.")
    return [[a + b for a, b in zip(row_a, row_b)] for row_a, row_b in zip(A, B)]


def subtract(A: Matrix, B: Matrix) -> Matrix:
    if not same_shape(A, B):
        raise ValueError("Matrices must have the same shape.")
    return [[a - b for a, b in zip(row_a, row_b)] for row_a, row_b in zip(A, B)]


def scale(alpha: float, A: Matrix) -> Matrix:
    return [[alpha * value for value in row] for row in A]


def linear_combination(alpha: float, A: Matrix, beta: float, B: Matrix) -> Matrix:
    return add(scale(alpha, A), scale(beta, B))


def entry_sum(matrix: Matrix) -> float:
    return sum(sum(row) for row in matrix)


def build_audit() -> MatrixArithmeticAudit:
    baseline = [
        [10.0, 2.0, 0.0],
        [1.0, 12.0, 3.0],
        [0.0, 4.0, 8.0],
    ]

    intervention_effect = [
        [1.0, 0.5, 0.0],
        [0.2, 1.5, 0.4],
        [0.0, 0.7, 1.2],
    ]

    stress_effect = [
        [-0.5, -0.2, 0.0],
        [-0.1, -0.8, -0.3],
        [0.0, -0.4, -0.9],
    ]

    combined_change = linear_combination(1.0, intervention_effect, 0.5, stress_effect)
    future = add(baseline, combined_change)
    difference = subtract(future, baseline)

    return MatrixArithmeticAudit(
        operation_name="baseline_plus_weighted_intervention_and_stress",
        matrix_shape=f"{shape(baseline)[0]}x{shape(baseline)[1]}",
        row_meaning="infrastructure subsystem",
        column_meaning="performance relationship or dependency category",
        units="normalized condition-effect score",
        weights="1.0 intervention effect plus 0.5 stress effect",
        compatible_shape=same_shape(baseline, intervention_effect, stress_effect),
        output_entry_sum=round(entry_sum(difference), 4),
        interpretation_warning=(
            "The arithmetic is shape-compatible, but the weighted combination is meaningful "
            "only if rows, columns, units, baselines, and effect definitions align."
        ),
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "matrix_arithmetic_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "matrix_arithmetic_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Matrix arithmetic audit complete.")


if __name__ == "__main__":
    main()
