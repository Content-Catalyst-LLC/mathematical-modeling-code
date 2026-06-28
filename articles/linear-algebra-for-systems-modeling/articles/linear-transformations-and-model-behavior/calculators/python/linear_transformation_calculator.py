from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "calculator": "linear_transformation_calculator",
        "row_count": 3,
        "column_count": 3,
        "input_state": "100.000000,60.000000,30.000000",
        "output_state": "126.000000,75.500000,42.000000",
        "rank": 3,
        "nullity": 0,
        "input_norm": 120.415946,
        "output_norm": 152.750205,
        "amplification_ratio": 1.268531,
        "warning": "Matrix action shows modeled behavior; row meanings, column meanings, units, scaling, and sensitivity still require review."
    }

    with (output_dir / "linear_transformation_calculator.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    with (output_dir / "linear_transformation_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
