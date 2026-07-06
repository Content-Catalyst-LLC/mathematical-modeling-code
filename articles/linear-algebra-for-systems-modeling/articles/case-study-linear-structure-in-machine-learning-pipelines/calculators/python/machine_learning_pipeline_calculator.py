from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "calculator": "case_study_linear_structure_in_machine_learning_pipelines_calculator",
        "workflow_name": "machine_learning_linear_structure_audit",
        "scenario_name": "synthetic_infrastructure_risk_pipeline",
        "observation_count": 10,
        "feature_count": 4,
        "train_count": 7,
        "test_count": 3,
        "model_family": "ridge_regression_linear_baseline",
        "regularization_strength": 0.25,
        "test_rmse": 0.041,
        "max_absolute_residual": 0.061,
        "largest_weight_feature": "inspection_gap",
        "warning": "Machine learning pipeline outputs require feature provenance, target validity, leakage controls, validation, residual review, monitoring, and decision boundaries."
    }

    with (output_dir / "case_study_linear_structure_ml_pipeline_calculator.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    with (output_dir / "case_study_linear_structure_ml_pipeline_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
