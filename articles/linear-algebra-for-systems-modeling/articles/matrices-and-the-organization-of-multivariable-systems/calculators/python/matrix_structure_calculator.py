from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    matrix = [
        [0.0, 2.0, 0.0, 1.0],
        [2.0, 0.0, 3.0, 0.0],
        [0.0, 3.0, 0.0, 4.0],
        [1.0, 0.0, 4.0, 0.0],
    ]
    row_count = len(matrix)
    column_count = len(matrix[0])
    entry_count = row_count * column_count
    nonzero_entries = sum(1 for row in matrix for value in row if value != 0)
    symmetric = all(matrix[i][j] == matrix[j][i] for i in range(row_count) for j in range(column_count))

    result = {
        "calculator": "matrix_structure_calculator",
        "row_count": row_count,
        "column_count": column_count,
        "nonzero_entries": nonzero_entries,
        "sparsity_ratio": round(1 - nonzero_entries / entry_count, 4),
        "symmetric": symmetric,
        "warning": "Matrix structure should be interpreted through row, column, and entry meaning."
    }

    with (output_dir / "matrix_structure_calculator.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    with (output_dir / "matrix_structure_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
