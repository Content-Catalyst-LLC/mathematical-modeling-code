from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    rows = [
        {
            "calculator": "numerical_stability_and_conditioning_calculator",
            "matrix_case": "well_conditioned_system",
            "determinant": 5.75,
            "condition_number_proxy": 2.10,
            "residual_norm": 0.0,
            "perturbation_size": 0.00001,
            "perturbed_solution_change": 0.000004,
            "stability_status": "stable_under_demo_threshold",
            "warning": "Residuals should be interpreted alongside conditioning, scaling, perturbation sensitivity, solver method, precision, and model purpose."
        },
        {
            "calculator": "numerical_stability_and_conditioning_calculator",
            "matrix_case": "ill_conditioned_system",
            "determinant": 0.00000001,
            "condition_number_proxy": 399920000.0,
            "residual_norm": 0.0,
            "perturbation_size": 0.00001,
            "perturbed_solution_change": 2000.0,
            "stability_status": "review_required_ill_conditioned",
            "warning": "Residuals should be interpreted alongside conditioning, scaling, perturbation sensitivity, solver method, precision, and model purpose."
        }
    ]

    with (output_dir / "numerical_stability_and_conditioning_calculator.json").open("w", encoding="utf-8") as handle:
        json.dump(rows, handle, indent=2, sort_keys=True)

    with (output_dir / "numerical_stability_and_conditioning_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(json.dumps(rows, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
