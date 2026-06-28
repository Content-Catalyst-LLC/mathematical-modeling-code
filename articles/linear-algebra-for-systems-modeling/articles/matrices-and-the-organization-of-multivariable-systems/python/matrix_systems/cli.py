from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class MatrixStructureAudit:
    matrix_name: str
    matrix_role: str
    row_meaning: str
    column_meaning: str
    row_count: int
    column_count: int
    nonzero_entries: int
    sparsity_ratio: float
    symmetric: bool
    rank: int
    interpretation_warning: str


def matrix_rank(matrix: list[list[float]], tolerance: float = 1e-10) -> int:
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


def is_symmetric(matrix: list[list[float]], tolerance: float = 1e-10) -> bool:
    if not matrix or len(matrix) != len(matrix[0]):
        return False
    n = len(matrix)
    return all(abs(matrix[i][j] - matrix[j][i]) <= tolerance for i in range(n) for j in range(n))


def sample_matrix() -> list[list[float]]:
    return [
        [0.0, 2.0, 0.0, 1.0],
        [2.0, 0.0, 3.0, 0.0],
        [0.0, 3.0, 0.0, 4.0],
        [1.0, 0.0, 4.0, 0.0],
    ]


def build_audit() -> MatrixStructureAudit:
    matrix = sample_matrix()
    row_count = len(matrix)
    column_count = len(matrix[0])
    entry_count = row_count * column_count
    nonzero_entries = sum(1 for row in matrix for value in row if value != 0)
    sparsity_ratio = 1.0 - (nonzero_entries / entry_count)

    return MatrixStructureAudit(
        matrix_name="infrastructure_interdependency_matrix",
        matrix_role="weighted adjacency matrix",
        row_meaning="infrastructure subsystem receiving or indexed by relationship",
        column_meaning="infrastructure subsystem sending or paired by relationship",
        row_count=row_count,
        column_count=column_count,
        nonzero_entries=nonzero_entries,
        sparsity_ratio=round(sparsity_ratio, 4),
        symmetric=is_symmetric(matrix),
        rank=matrix_rank(matrix),
        interpretation_warning=(
            "Symmetry suggests reciprocal relationships in this example, but real "
            "infrastructure dependencies may be directional and should not be assumed symmetric."
        ),
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "matrix_structure_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "matrix_structure_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Matrix structure audit complete.")


if __name__ == "__main__":
    main()
