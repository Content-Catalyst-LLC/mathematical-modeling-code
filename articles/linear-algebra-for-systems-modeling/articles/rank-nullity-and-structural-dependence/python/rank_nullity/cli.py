from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path

Matrix = list[list[float]]


@dataclass(frozen=True)
class RankNullityAudit:
    system_name: str
    row_count: int
    column_count: int
    rank: int
    nullity: int
    rank_deficient: bool
    pivot_columns: str
    free_columns: str
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


def build_audit() -> RankNullityAudit:
    A = [
        [1.0, 1.0, 0.0],
        [0.0, 1.0, 1.0],
        [1.0, 0.0, 1.0],
    ]

    tolerance = 1e-10
    _, pivots = rref(A, tolerance=tolerance)
    row_count = len(A)
    column_count = len(A[0])
    rank = len(pivots)
    nullity = column_count - rank
    maximum_rank = min(row_count, column_count)
    free_columns = [column for column in range(column_count) if column not in pivots]

    return RankNullityAudit(
        system_name="three_constraint_resource_balance_matrix",
        row_count=row_count,
        column_count=column_count,
        rank=rank,
        nullity=nullity,
        rank_deficient=rank < maximum_rank,
        pivot_columns=",".join(str(column) for column in pivots),
        free_columns=",".join(str(column) for column in free_columns) if free_columns else "none",
        tolerance=tolerance,
        interpretation_warning=(
            "Rank and nullity reveal algebraic structure, but dependence and freedom "
            "must be interpreted using row meanings, column meanings, units, and modeling purpose."
        ),
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "rank_nullity_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "rank_nullity_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Rank-nullity audit complete.")


if __name__ == "__main__":
    main()
