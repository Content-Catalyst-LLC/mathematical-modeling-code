from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "calculator": "linear_system_consistency_calculator",
        "equation_count": 3,
        "unknown_count": 3,
        "coefficient_rank": 3,
        "augmented_rank": 3,
        "consistent": True,
        "solution_behavior": "unique solution",
        "warning": "Consistency does not guarantee practical feasibility."
    }

    with (output_dir / "linear_system_calculator.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    with (output_dir / "linear_system_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
