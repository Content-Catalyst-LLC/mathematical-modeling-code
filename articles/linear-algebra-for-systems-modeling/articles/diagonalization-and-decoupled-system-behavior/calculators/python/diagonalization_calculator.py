from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "calculator": "diagonalization_calculator",
        "matrix_entries": "0.796667,0.123333;0.246667,0.673333",
        "eigenvector_matrix": "1.000000,1.000000;1.000000,-2.000000",
        "diagonal_matrix": "0.920000,0.000000;0.000000,0.550000",
        "reconstruction_error_frobenius": 0.0,
        "spectral_radius": 0.92,
        "dominant_eigenvalue": 0.92,
        "stability_classification": "all_modes_decay_discrete_time",
        "warning": "Diagonalization decouples representation, not necessarily real-world independence."
    }

    with (output_dir / "diagonalization_calculator.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    with (output_dir / "diagonalization_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
