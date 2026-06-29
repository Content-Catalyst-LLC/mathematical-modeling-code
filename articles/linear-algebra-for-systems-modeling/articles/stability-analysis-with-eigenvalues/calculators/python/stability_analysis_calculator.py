from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "calculator": "stability_analysis_calculator",
        "matrix_entries": "0.820000,0.120000;0.180000,0.760000",
        "eigenvalue_1": 0.94,
        "eigenvalue_2": 0.64,
        "spectral_radius": 0.94,
        "largest_real_part": 0.94,
        "discrete_time_classification": "asymptotically_stable_discrete_time",
        "continuous_time_classification": "unstable_continuous_time",
        "warning": "Discrete-time stability uses eigenvalue magnitudes relative to one; continuous-time stability uses real parts relative to zero."
    }

    with (output_dir / "stability_analysis_calculator.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    with (output_dir / "stability_analysis_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
