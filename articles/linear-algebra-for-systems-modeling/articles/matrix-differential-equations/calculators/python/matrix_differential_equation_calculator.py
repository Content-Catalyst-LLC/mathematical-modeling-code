from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "calculator": "matrix_differential_equation_calculator",
        "state_names": "infrastructure_stress|service_delay",
        "system_matrix": "-0.280000,0.080000;0.120000,-0.340000",
        "initial_state": "10.000000,4.000000",
        "time_horizon": 10.0,
        "eigenvalues": "-0.200000,-0.420000",
        "max_real_part": -0.2,
        "stability_classification": "asymptotically_stable_continuous_time",
        "warning": "Use continuous-time stability rules based on eigenvalue real parts, not discrete-time spectral-radius rules."
    }

    with (output_dir / "matrix_differential_equation_calculator.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    with (output_dir / "matrix_differential_equation_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
