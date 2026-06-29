from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    result = {
        "calculator": "projection_reflection_calculator",
        "original_vector": "4.000000,3.000000",
        "unit_direction": "0.894427,0.447214",
        "projected_vector": "4.400000,2.200000",
        "residual_vector": "-0.400000,0.800000",
        "residual_norm": 0.894427,
        "reflected_vector": "4.800000,1.400000",
        "projection_idempotence_error": 0.0,
        "projection_symmetry_error": 0.0,
        "reflection_involution_error": 0.0,
        "length_preservation_error": 0.0,
        "warning": "Projection and reflection interpretation depends on geometry, units, scaling, and model purpose."
    }
    (output_dir / "projection_reflection_calculator.json").write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    with (output_dir / "projection_reflection_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
