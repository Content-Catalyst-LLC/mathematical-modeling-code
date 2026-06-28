from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path

Matrix = list[list[float]]
Vector = list[float]


@dataclass(frozen=True)
class LinearSystemAudit:
    system_name: str
    equation_count: int
    unknown_count: int
    coefficient_rank: int
    augmented_rank: int
    consistent: bool
    solution_behavior: str
    row_meaning: str
    column_meaning: str
    right_hand_side_meaning: str
    interpretation_warning: str


def matrix_rank(matrix: Matrix, tolerance: float = 1e-10) -> int:
    rows = [row[:] for row in matrix]
    row_count = len(rows)
    column_count = len(rows[0]) if rows else 0
    rank = 0

    for column in range(column_count):
        pivot = None
        for row in range(rank, row_count):
            if abs(rows[row][column]) > tolerance:
                pivot = row
                break

        if pivot is None:
            continue

        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        pivot_value = rows[rank][column]
        rows[rank] = [value / pivot_value for value in rows[rank]]

        for row in range(row_count):
            if row != rank:
                factor = rows[row][column]
                rows[row] = [
                    current - factor * pivot_current
                    for current, pivot_current in zip(rows[row], rows[rank])
                ]

        rank += 1

    return rank


def augment(A: Matrix, b: Vector) -> Matrix:
    return [row + [rhs] for row, rhs in zip(A, b)]


def classify_solution_behavior(A: Matrix, b: Vector) -> tuple[bool, str, int, int]:
    coefficient_rank = matrix_rank(A)
    augmented_rank = matrix_rank(augment(A, b))
    unknown_count = len(A[0]) if A else 0

    if coefficient_rank != augmented_rank:
        return False, "no solution", coefficient_rank, augmented_rank

    if coefficient_rank == unknown_count:
        return True, "unique solution", coefficient_rank, augmented_rank

    return True, "infinitely many solutions", coefficient_rank, augmented_rank


def build_audit() -> LinearSystemAudit:
    A = [
        [1.0, 1.0, 0.0],
        [0.0, 1.0, 1.0],
        [1.0, 0.0, 1.0],
    ]
    b = [100.0, 80.0, 90.0]

    consistent, behavior, rank_a, rank_aug = classify_solution_behavior(A, b)

    return LinearSystemAudit(
        system_name="three_constraint_resource_balance_system",
        equation_count=len(A),
        unknown_count=len(A[0]),
        coefficient_rank=rank_a,
        augmented_rank=rank_aug,
        consistent=consistent,
        solution_behavior=behavior,
        row_meaning="resource balance constraints",
        column_meaning="unknown allocation levels",
        right_hand_side_meaning="required total resource targets",
        interpretation_warning=(
            "The linear system may be algebraically consistent, but practical feasibility "
            "also requires nonnegative allocations, capacity limits, and policy constraints."
        ),
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "linear_system_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "linear_system_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Linear system audit complete.")


if __name__ == "__main__":
    main()
