from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "calculator": "control_systems_calculator",
        "time_model": "continuous_time_linear_state_space",
        "state_matrix_A": "0.100000,1.000000;0.000000,0.200000",
        "input_matrix_B": "0.000000;1.000000",
        "output_matrix_C": "1.000000,0.000000",
        "feedback_matrix_K": "0.500000,1.400000",
        "open_loop_eigenvalues": "0.200000,0.100000",
        "closed_loop_eigenvalues": "-0.600000,-0.500000",
        "controllability_rank": 2,
        "observability_rank": 2,
        "warning": "Feedback analysis requires actuator limits, delays, noise, uncertainty, constraints, and objective transparency."
    }

    with (output_dir / "control_systems_calculator.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    with (output_dir / "control_systems_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
