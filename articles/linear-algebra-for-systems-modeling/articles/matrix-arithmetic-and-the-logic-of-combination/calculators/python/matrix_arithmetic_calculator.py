from __future__ import annotations

import csv
import json
from pathlib import Path


def add(A, B):
    return [[a + b for a, b in zip(row_a, row_b)] for row_a, row_b in zip(A, B)]


def scale(alpha, A):
    return [[alpha * value for value in row] for row in A]


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    baseline = [
        [10.0, 2.0, 0.0],
        [1.0, 12.0, 3.0],
        [0.0, 4.0, 8.0],
    ]
    intervention = [
        [1.0, 0.5, 0.0],
        [0.2, 1.5, 0.4],
        [0.0, 0.7, 1.2],
    ]
    stress = [
        [-0.5, -0.2, 0.0],
        [-0.1, -0.8, -0.3],
        [0.0, -0.4, -0.9],
    ]

    combined_change = add(intervention, scale(0.5, stress))
    future = add(baseline, combined_change)

    result = {
        "calculator": "matrix_arithmetic_calculator",
        "shape": "3x3",
        "intervention_weight": 1.0,
        "stress_weight": 0.5,
        "combined_change_total": round(sum(sum(row) for row in combined_change), 4),
        "future_total": round(sum(sum(row) for row in future), 4),
        "warning": "Shape compatibility does not prove semantic compatibility."
    }

    with (output_dir / "matrix_arithmetic_calculator.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    with (output_dir / "matrix_arithmetic_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
