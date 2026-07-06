from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "calculator": "case_study_infrastructure_interdependence_calculator",
        "workflow_name": "infrastructure_interdependence_audit",
        "scenario_name": "synthetic_power_disruption_dependency_scenario",
        "sector_count": 5,
        "initial_shock_sector": "power",
        "initial_shock_magnitude": 0.40,
        "highest_dependency_burden_sector": "power",
        "highest_dependency_burden": 2.40,
        "largest_downstream_loss_sector": "health",
        "largest_downstream_loss": 0.32,
        "total_estimated_downstream_loss": 0.96,
        "warning": "Dependency weights are scenario assumptions and cascade estimates require validation."
    }

    with (output_dir / "case_study_infrastructure_interdependence_calculator.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    with (output_dir / "case_study_infrastructure_interdependence_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
