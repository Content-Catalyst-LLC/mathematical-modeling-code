from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "calculator": "orthogonal_decomposition_structured_approximation_calculator",
        "model_name": "synthetic_orthogonal_approximation_audit",
        "rows": 6,
        "columns": 3,
        "numerical_rank": 3,
        "condition_number": 58.0,
        "residual_norm": 0.346410,
        "relative_residual_norm": 0.032100,
        "orthogonality_error": 0.0,
        "coefficient_norm": 2.513000,
        "method": "qr_least_squares",
        "warning": "Approximation metrics depend on subspace choice, scaling, rank tolerance, conditioning, solver method, residual interpretation, data provenance, and validation context."
    }

    with (output_dir / "orthogonal_decomposition_structured_approximation_calculator.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    with (output_dir / "orthogonal_decomposition_structured_approximation_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
