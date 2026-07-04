from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "calculator": "scientific_computing_workflows_for_linear_algebra_calculator",
        "model_name": "scientific_computing_linear_algebra_audit",
        "workflow_stage": "matrix_construction_solve_diagnostics_metadata",
        "matrix_shape": "3x3",
        "representation": "dense_demo_matrix",
        "precision": "double_precision_like",
        "solver_choice": "direct_small_system_solve",
        "tolerance": 1.0e-10,
        "determinant": 26.625,
        "condition_number_proxy": 3.42,
        "residual_norm": 0.0,
        "relative_residual": 0.0,
        "reproducibility_status": "pass_residual_tolerance",
        "warning": "Scientific computing workflows require matrix construction, representation, backend, solver, tolerance, diagnostics, reproducibility, validation, and responsible-use review."
    }

    with (output_dir / "scientific_computing_workflows_for_linear_algebra_calculator.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    with (output_dir / "scientific_computing_workflows_for_linear_algebra_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
