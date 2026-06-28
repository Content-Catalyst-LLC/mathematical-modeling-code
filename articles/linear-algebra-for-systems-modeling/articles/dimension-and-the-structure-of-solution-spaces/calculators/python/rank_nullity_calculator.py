from __future__ import annotations

import csv
import json
from pathlib import Path


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


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    matrix = [
        [1.0, 1.0, 0.0, 0.0],
        [0.0, 1.0, 1.0, 0.0],
        [0.0, 0.0, 1.0, 1.0],
    ]
    variable_count = len(matrix[0])
    equation_count = len(matrix)
    rank = matrix_rank(matrix)
    nullity = variable_count - rank

    result = {
        "calculator": "rank_nullity_calculator",
        "variable_count": variable_count,
        "equation_count": equation_count,
        "rank": rank,
        "nullity": nullity,
        "likely_solution_structure": "positive_dimensional_if_consistent" if nullity > 0 else "unique_if_consistent",
        "warning": "Rank-nullity describes mathematical freedom, not feasibility or adequacy."
    }

    with (output_dir / "rank_nullity_calculator.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    with (output_dir / "rank_nullity_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
