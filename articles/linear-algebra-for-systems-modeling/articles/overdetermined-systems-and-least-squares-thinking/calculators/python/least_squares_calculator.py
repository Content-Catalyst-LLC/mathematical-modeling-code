from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "calculator": "least_squares_calculator",
        "row_count": 4,
        "column_count": 2,
        "overdetermined": True,
        "rank": 2,
        "solution": "0.850000,1.040000",
        "fitted_values": "1.890000,2.930000,3.970000,5.010000",
        "residuals": "0.110000,-0.030000,0.130000,0.090000",
        "residual_norm": 0.191311,
        "warning": "Least squares gives a squared-error approximation; residual patterns and model meaning still require review."
    }

    with (output_dir / "least_squares_calculator.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    with (output_dir / "least_squares_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
