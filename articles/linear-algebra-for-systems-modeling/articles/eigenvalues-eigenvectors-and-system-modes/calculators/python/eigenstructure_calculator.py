from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "calculator": "eigenstructure_calculator",
        "matrix_entries": "0.820000,0.120000;0.180000,0.760000",
        "trace": 1.58,
        "determinant": 0.6016,
        "eigenvalue_1": 0.94,
        "eigenvalue_2": 0.64,
        "spectral_radius": 0.94,
        "dominant_eigenvalue": 0.94,
        "stability_classification": "asymptotically_damped_discrete_time",
        "warning": "Eigenvalues describe modes of the specified matrix, not automatic causal mechanisms."
    }

    with (output_dir / "eigenstructure_calculator.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    with (output_dir / "eigenstructure_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
