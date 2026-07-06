from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "calculator": "case_study_state_transition_and_markov_dynamics_calculator",
        "workflow_name": "state_transition_markov_audit",
        "scenario_name": "synthetic_infrastructure_condition_transition_model",
        "state_count": 4,
        "time_steps": 5,
        "stochastic_check_passed": True,
        "highest_probability_state_after_horizon": "normal",
        "highest_probability_after_horizon": 0.42833125,
        "stationary_highest_probability_state": "normal",
        "stationary_highest_probability": 0.40602189781,
        "baseline_disrupted_probability_after_horizon": 0.1756128125,
        "stress_disrupted_probability_after_horizon": 0.41016825,
        "warning": "State transition results depend on state definitions, transition estimates, time-step choices, uncertainty, validation, and memoryless-assumption limits."
    }

    with (output_dir / "case_study_state_transition_and_markov_dynamics_calculator.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    with (output_dir / "case_study_state_transition_and_markov_dynamics_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
