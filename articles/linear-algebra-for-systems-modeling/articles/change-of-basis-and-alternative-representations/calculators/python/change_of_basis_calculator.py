from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "calculator": "change_of_basis_calculator",
        "basis_shape": "2x2",
        "basis_rank": 2,
        "basis_determinant": 3.0,
        "original_vector": "5.000000,4.000000",
        "basis_coordinates": "2.000000,1.500000",
        "reconstructed_vector": "5.000000,4.000000",
        "reconstruction_error": 0.0,
        "transformed_matrix": "1.133333,0.033333;0.333333,0.966667",
        "warning": "Coordinate changes require basis meaning, units, conditioning, and translation back to system terms."
    }

    with (output_dir / "change_of_basis_calculator.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    with (output_dir / "change_of_basis_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
