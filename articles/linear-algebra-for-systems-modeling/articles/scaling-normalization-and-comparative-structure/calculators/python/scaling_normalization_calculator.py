from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "calculator": "scaling_normalization_and_comparative_structure_calculator",
        "workflow_name": "scaling_normalization_audit",
        "matrix_shape": "3x2",
        "row_meaning": "infrastructure_zones",
        "column_meaning": "annual_demand_and_outage_exposure",
        "raw_column_norm_1": 2345.207880,
        "raw_column_norm_2": 0.174929,
        "standardized_column_norm_1": 1.414214,
        "standardized_column_norm_2": 1.414214,
        "first_row_sum_after_row_normalization": 1.0,
        "first_row_norm_after_unit_normalization": 1.0,
        "raw_condition_proxy": 13406.312329,
        "standardized_condition_proxy": 1.0,
        "warning": "Scaling and normalization change whether the model compares magnitude, relative position, composition, direction, probability, or numerical balance."
    }

    with (output_dir / "scaling_normalization_and_comparative_structure_calculator.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    with (output_dir / "scaling_normalization_and_comparative_structure_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
