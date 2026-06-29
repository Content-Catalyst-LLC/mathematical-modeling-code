from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "calculator": "orthogonality_calculator",
        "vector_a": "3.000000,1.000000,2.000000",
        "vector_b": "1.000000,-1.000000,-1.000000",
        "dot_product": 0.0,
        "orthogonal_under_tolerance": True,
        "unit_a": "0.801784,0.267261,0.534522",
        "unit_b": "0.577350,-0.577350,-0.577350",
        "projection_of_a_onto_b": "0.000000,0.000000,0.000000",
        "residual_vector": "3.000000,1.000000,2.000000",
        "residual_norm": 3.741657,
        "orthonormality_error": 0.0,
        "warning": "Orthogonality depends on geometry, scaling, units, tolerance, and domain interpretation."
    }

    with (output_dir / "orthogonality_calculator.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    with (output_dir / "orthogonality_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
