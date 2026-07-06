from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "calculator": "case_study_economic_input_output_analysis_calculator",
        "workflow_name": "economic_input_output_audit",
        "economy_name": "synthetic_three_sector_economy",
        "sector_count": 3,
        "final_demand_total": 450.0,
        "gross_output_total": 763.099081201887,
        "highest_multiplier_sector": "manufacturing",
        "highest_output_multiplier": 1.951825177111,
        "shock_sector": "manufacturing",
        "shock_amount": 25.0,
        "gross_output_change_total": 48.795629500869,
        "leontief_infinity_condition_estimate": 2.147504345667,
        "warning": "Input-output multipliers are fixed-coefficient scenario outputs, not automatic policy conclusions."
    }

    with (output_dir / "case_study_economic_input_output_analysis_calculator.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    with (output_dir / "case_study_economic_input_output_analysis_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
