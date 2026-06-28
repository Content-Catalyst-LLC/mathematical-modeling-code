from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path

Matrix = list[list[float]]


@dataclass(frozen=True)
class PivotStructureAudit:
    system_name: str
    equation_count: int
    unknown_count: int
    pivot_columns: str
    free_columns: str
    coefficient_rank: int
    augmented_rank: int
    consistent: bool
    solution_behavior: str
    tolerance: float
    interpretation_warning: str


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

    cleaned = [
        [0.0 if abs(value) < tolerance else round(value, 10) for value in row]
        for row in rows
    ]
    return cleaned, pivot_columns


def rank_from_rref(reduced: Matrix, coefficient_columns: int, tolerance: float = 1e-10) -> int:
    return sum(
        1
        for row in reduced
        if any(abs(value) > tolerance for value in row[:coefficient_columns])
    )


def augmented_rank_from_rref(reduced: Matrix, tolerance: float = 1e-10) -> int:
    return sum(1 for row in reduced if any(abs(value) > tolerance for value in row))


def classify_solution_behavior(coefficient_rank: int, augmented_rank: int, unknown_count: int) -> tuple[bool, str]:
    if coefficient_rank != augmented_rank:
        return False, "no solution"
    if coefficient_rank == unknown_count:
        return True, "unique solution"
    return True, "infinitely many solutions"


def build_audit() -> PivotStructureAudit:
    augmented = [
        [1.0, 1.0, 0.0, 100.0],
        [0.0, 1.0, 1.0, 80.0],
        [1.0, 0.0, 1.0, 90.0],
    ]

    tolerance = 1e-10
    unknown_count = 3
    reduced, all_pivots = rref(augmented, tolerance=tolerance)

    variable_pivots = [column for column in all_pivots if column < unknown_count]
    free_columns = [column for column in range(unknown_count) if column not in variable_pivots]

    coefficient_rank = rank_from_rref(reduced, coefficient_columns=unknown_count, tolerance=tolerance)
    augmented_rank = augmented_rank_from_rref(reduced, tolerance=tolerance)

    consistent, behavior = classify_solution_behavior(coefficient_rank, augmented_rank, unknown_count)

    return PivotStructureAudit(
        system_name="three_constraint_resource_balance_system",
        equation_count=len(augmented),
        unknown_count=unknown_count,
        pivot_columns=",".join(str(column) for column in variable_pivots),
        free_columns=",".join(str(column) for column in free_columns) if free_columns else "none",
        coefficient_rank=coefficient_rank,
        augmented_rank=augmented_rank,
        consistent=consistent,
        solution_behavior=behavior,
        tolerance=tolerance,
        interpretation_warning=(
            "Pivot structure reveals algebraic solvability, but practical feasibility "
            "depends on original equation meaning, units, constraints, and data quality."
        ),
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "pivot_structure_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "pivot_structure_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Pivot structure audit complete.")


if __name__ == "__main__":
    main()
