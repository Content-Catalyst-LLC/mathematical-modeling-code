from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "calculator": "decomposition_workflows_for_systems_analysis_calculator",
        "model_name": "decomposition_workflow_audit",
        "matrix_shape": "4x3",
        "matrix_class": "rectangular_overdetermined_dense_demo_matrix",
        "recommended_workflow": "QR_or_SVD_for_least_squares_and_rank_diagnostics",
        "condition_proxy": 4.2,
        "estimated_rank": 3,
        "singular_value_1": 5.12,
        "singular_value_2": 2.35,
        "singular_value_3": 1.02,
        "low_rank_reconstruction_error": 1.02,
        "solve_residual_norm": 0.0,
        "warning": "Decomposition workflows require matrix-structure review, rank tolerance, reconstruction error, residual diagnostics, conditioning, approximation limits, and interpretation boundaries."
    }

    with (output_dir / "decomposition_workflows_for_systems_analysis_calculator.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    with (output_dir / "decomposition_workflows_for_systems_analysis_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
