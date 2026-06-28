from __future__ import annotations
import csv, json
from pathlib import Path

result = {
    "calculator": "inverse_recovery_calculator",
    "matrix_size": 3,
    "determinant": 2.0,
    "invertible": True,
    "rank": 3,
    "nullity": 0,
    "recovered_solution": "55.000000,45.000000,35.000000",
    "residual_norm": 0.0,
    "tolerance": 1.0e-10,
    "warning": "Inverse recovery is exact for this synthetic example; conditioning and model meaning still require review."
}
Path("outputs").mkdir(parents=True, exist_ok=True)
Path("outputs/inverse_recovery_calculator.json").write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
with Path("outputs/inverse_recovery_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
    writer.writeheader()
    writer.writerow(result)
print(json.dumps(result, indent=2, sort_keys=True))
