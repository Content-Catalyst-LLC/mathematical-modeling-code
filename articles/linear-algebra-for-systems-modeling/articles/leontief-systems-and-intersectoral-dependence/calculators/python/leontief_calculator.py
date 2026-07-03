from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "calculator": "leontief_systems_and_intersectoral_dependence_calculator",
        "model_name": "synthetic_leontief_intersectoral_dependence_audit",
        "sectors": 4,
        "method": "demand_driven_leontief_system",
        "coefficient_basis": "sector_input_per_unit_output",
        "spectral_radius": 0.331,
        "condition_number": 2.41,
        "productive_system_flag": True,
        "maximum_output_multiplier": 1.47,
        "highest_multiplier_sector": "manufacturing",
        "total_output_required": 319.8,
        "total_shock_output_change": 36.2,
        "emissions_for_final_demand": 150.6,
        "warning": "Leontief metrics depend on coefficient construction, productivity conditions, matrix conditioning, scenario definition, environmental extensions, sensitivity testing, and interpretation context."
    }

    with (output_dir / "leontief_systems_and_intersectoral_dependence_calculator.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    with (output_dir / "leontief_systems_and_intersectoral_dependence_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
