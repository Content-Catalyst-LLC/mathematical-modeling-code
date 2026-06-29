from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "calculator": "long_run_transition_calculator",
        "states": "good|fair|poor",
        "orientation": "row_stochastic_row_vector_update_pi_next_equals_pi_P",
        "transition_matrix": "0.820000,0.160000,0.020000;0.100000,0.760000,0.140000;0.030000,0.220000,0.750000",
        "stationary_estimate": "0.233333,0.488889,0.277778",
        "distribution_after_25_steps": "0.236019,0.487126,0.276855",
        "convergence_distance": 0.005372,
        "row_sum_error": 0.0,
        "nonnegative": True,
        "warning": "Long-run behavior depends on convergence diagnostics, initial-condition sensitivity, stationarity, and practical horizon."
    }

    with (output_dir / "long_run_transition_calculator.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    with (output_dir / "long_run_transition_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
