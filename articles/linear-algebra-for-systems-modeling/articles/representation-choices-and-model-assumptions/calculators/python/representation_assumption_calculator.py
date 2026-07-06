from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "calculator": "representation_choices_and_model_assumptions_calculator",
        "workflow_name": "representation_assumption_audit",
        "matrix_shape": "3x2",
        "row_meaning": "infrastructure_zones",
        "column_meaning": "annual_demand_and_outage_exposure",
        "value_meaning": "mixed_units_before_standardization",
        "zero_meaning": "zero_would_mean_measured_absence_not_missingness",
        "raw_column_norm_1": 2345.207880,
        "raw_column_norm_2": 0.174929,
        "standardized_column_norm_1": 1.414214,
        "standardized_column_norm_2": 1.414214,
        "warning": "Representation choices define what the model can compare, reveal, hide, and justify."
    }

    with (output_dir / "representation_choices_and_model_assumptions_calculator.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    with (output_dir / "representation_choices_and_model_assumptions_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
