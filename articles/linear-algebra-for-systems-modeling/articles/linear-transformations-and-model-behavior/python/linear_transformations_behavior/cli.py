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
class TransformationBehaviorAudit:
    system_name: str
    row_count: int
    column_count: int
    input_state: str
    output_state: str
    rank: int
    nullity: int
    input_norm: float
    output_norm: float
    amplification_ratio: float
    behavior_warning: str
    interpretation_warning: str


def matvec(A: Matrix, x: Vector) -> Vector:
    return [sum(a * b for a, b in zip(row, x)) for row in A]


def norm2(v: Vector) -> float:
    return math.sqrt(sum(value * value for value in v))


def rref(matrix: Matrix, tolerance: float = 1e-10) -> tuple[Matrix, list[int]]:
    rows = [row[:] for row in matrix]
    row_count = len(rows)
    column_count = len(rows[0]) if rows else 0
    pivot_columns: list[int] = []
    pivot_row = 0

    for column in range(column_count):
        pivot = None
        for row in range(pivot_row, row_count):
            if abs(rows[row][column]) > tolerance:
                pivot = row
                break

        if pivot is None:
            continue

        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        pivot_value = rows[pivot_row][column]
        rows[pivot_row] = [value / pivot_value for value in rows[pivot_row]]

        for row in range(row_count):
            if row != pivot_row:
                factor = rows[row][column]
                rows[row] = [
                    current - factor * pivot_current
                    for current, pivot_current in zip(rows[row], rows[pivot_row])
                ]

        pivot_columns.append(column)
        pivot_row += 1

        if pivot_row == row_count:
            break

    return rows, pivot_columns


def build_audit() -> TransformationBehaviorAudit:
    A = [
        [1.20, 0.10, 0.00],
        [0.20, 0.85, 0.15],
        [0.00, 0.25, 0.90],
    ]
    x = [100.0, 60.0, 30.0]

    y = matvec(A, x)
    _, pivots = rref(A)
    rank = len(pivots)
    nullity = len(A[0]) - rank
    input_norm = norm2(x)
    output_norm = norm2(y)
    amplification_ratio = output_norm / input_norm if input_norm else float("nan")

    if amplification_ratio > 1.10:
        behavior_warning = "transformation amplifies this input state"
    elif amplification_ratio < 0.90:
        behavior_warning = "transformation dampens this input state"
    else:
        behavior_warning = "transformation keeps this input norm at a similar scale"

    return TransformationBehaviorAudit(
        system_name="three_component_system_response",
        row_count=len(A),
        column_count=len(A[0]),
        input_state=",".join(f"{value:.6f}" for value in x),
        output_state=",".join(f"{value:.6f}" for value in y),
        rank=rank,
        nullity=nullity,
        input_norm=round(input_norm, 12),
        output_norm=round(output_norm, 12),
        amplification_ratio=round(amplification_ratio, 12),
        behavior_warning=behavior_warning,
        interpretation_warning=(
            "Matrix action shows modeled behavior, but interpretation requires row meanings, "
            "column meanings, units, scaling, linearity assumptions, and sensitivity review."
        ),
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "linear_transformation_behavior_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "linear_transformation_behavior_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Linear transformation behavior audit complete.")


if __name__ == "__main__":
    main()
