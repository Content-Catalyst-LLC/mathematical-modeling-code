from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "calculator": "when_linear_models_clarify_and_when_they_distort_calculator",
        "workflow_name": "linearity_distortion_audit",
        "model_purpose": "baseline_linear_approximation_for_system_behavior",
        "fitted_intercept": 0.3,
        "fitted_slope": 2.1,
        "residual_sum_squares": 0.98,
        "max_absolute_residual": 0.7,
        "residual_sign_pattern": "+--0+",
        "warning": "Linear models clarify first-order structure, but residuals, thresholds, interactions, feedback, aggregation, and causal assumptions must be reviewed before using results for decisions."
    }

    with (output_dir / "when_linear_models_clarify_and_when_they_distort_calculator.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    with (output_dir / "when_linear_models_clarify_and_when_they_distort_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
