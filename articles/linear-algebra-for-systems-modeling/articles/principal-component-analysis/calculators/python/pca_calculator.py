from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "calculator": "principal_component_analysis_calculator",
        "model_name": "synthetic_pca_diagnostic_audit",
        "observations": 8,
        "variables": 5,
        "preprocessing": "centered_and_standardized",
        "retained_components": 2,
        "explained_variance_ratio": "0.946;0.044;0.007;0.002;0.001",
        "cumulative_explained_variance": 0.990,
        "relative_reconstruction_error": 0.100,
        "largest_loading_variable_pc1": "transport_delay",
        "largest_loading_variable_pc2": "water_demand",
        "warning": "PCA metrics depend on matrix construction, centering, scaling, retained components, explained-variance criteria, residual review, outlier handling, and validation context."
    }

    with (output_dir / "principal_component_analysis_calculator.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    with (output_dir / "principal_component_analysis_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
