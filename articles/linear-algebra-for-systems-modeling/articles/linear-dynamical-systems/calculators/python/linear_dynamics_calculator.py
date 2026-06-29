from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "calculator": "linear_dynamics_calculator",
        "state_names": "infrastructure_stress|service_delay",
        "update_matrix": "0.820000,0.120000;0.180000,0.760000",
        "initial_state": "10.000000,4.000000",
        "horizon": 20,
        "final_state": "3.626170,3.452104",
        "spectral_radius": 0.94,
        "stability_classification": "asymptotically_stable_discrete_time",
        "warning": "Linear dynamics depend on state definitions, units, scaling, time step, matrix validity, and whether linearity is structural or approximate."
    }

    with (output_dir / "linear_dynamics_calculator.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    with (output_dir / "linear_dynamics_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
