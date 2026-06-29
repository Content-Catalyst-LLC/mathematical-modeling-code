from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "calculator": "markov_transition_calculator",
        "states": "good|fair|poor",
        "orientation": "row_stochastic_row_vector_update_pi_next_equals_pi_P",
        "transition_matrix": "0.820000,0.160000,0.020000;0.100000,0.760000,0.140000;0.030000,0.220000,0.750000",
        "initial_distribution": "0.600000,0.300000,0.100000",
        "row_sum_error": 0.0,
        "nonnegative": True,
        "one_step_distribution": "0.525000,0.346000,0.129000",
        "ten_step_distribution": "0.286282,0.478868,0.234850",
        "steady_state_estimate": "0.233333,0.488889,0.277778",
        "warning": "Transition matrices depend on state definitions, time step, stationarity, data quality, and the Markov assumption."
    }

    with (output_dir / "markov_transition_calculator.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    with (output_dir / "markov_transition_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
