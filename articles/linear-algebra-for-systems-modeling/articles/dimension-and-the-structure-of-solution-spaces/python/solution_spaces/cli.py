from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class SolutionSpaceAudit:
    system_name: str
    variable_count: int
    equation_count: int
    rank: int
    nullity: int
    likely_solution_structure: str
    modeling_role: str
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


def build_audit() -> SolutionSpaceAudit:
    coefficient_matrix = [
        [1.0, 1.0, 0.0, 0.0],
        [0.0, 1.0, 1.0, 0.0],
        [0.0, 0.0, 1.0, 1.0],
    ]

    variable_count = len(coefficient_matrix[0])
    equation_count = len(coefficient_matrix)
    rank = matrix_rank(coefficient_matrix)
    nullity = variable_count - rank

    if nullity == 0:
        structure = "No free variables if the system is consistent; a unique solution may exist."
    else:
        structure = "Positive-dimensional solution space if the system is consistent."

    return SolutionSpaceAudit(
        system_name="four_variable_three_constraint_system",
        variable_count=variable_count,
        equation_count=equation_count,
        rank=rank,
        nullity=nullity,
        likely_solution_structure=structure,
        modeling_role="Audit degrees of freedom in a constrained system representation.",
        interpretation_warning=(
            "Rank and nullity describe mathematical freedom. Feasibility, data quality, "
            "and system meaning require separate review."
        ),
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "solution_space_audit.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "solution_space_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Solution space audit complete.")


if __name__ == "__main__":
    main()
