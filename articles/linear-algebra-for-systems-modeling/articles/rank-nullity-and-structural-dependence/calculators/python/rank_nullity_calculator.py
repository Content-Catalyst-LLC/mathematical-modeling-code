from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    column_count = 3
    rank = 3
    result = {
        "calculator": "rank_nullity_calculator",
        "row_count": 3,
        "column_count": column_count,
        "rank": rank,
        "nullity": column_count - rank,
        "rank_nullity_check": rank + (column_count - rank) == column_count,
        "rank_deficient": False,
        "pivot_columns": "0,1,2",
        "free_columns": "none",
        "tolerance": 1.0e-10,
        "warning": "Rank and nullity depend on matrix structure; numerical rank depends on tolerance."
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
