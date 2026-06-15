from __future__ import annotations
import argparse, csv, json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable

@dataclass(frozen=True)
class StabilityRecord:
    scenario: str
    equilibrium: float
    derivative_value: float
    stability: str
    domain_min: float
    domain_max: float
    warning: str

def logistic_rate(x: float, growth_rate: float, carrying_capacity: float) -> float:
    return growth_rate * x * (1.0 - x / carrying_capacity)

def logistic_derivative(x: float, growth_rate: float, carrying_capacity: float) -> float:
    return growth_rate * (1.0 - 2.0 * x / carrying_capacity)

def bistable_rate(x: float, threshold: float) -> float:
    return x * (1.0 - x) * (x - threshold)

def numerical_derivative(rate_function: Callable[[float], float], x: float, h: float = 1e-5) -> float:
    return (rate_function(x + h) - rate_function(x - h)) / (2.0 * h)

def classify_scalar_stability(derivative_value: float, tolerance: float = 1e-8) -> str:
    if derivative_value < -tolerance:
        return "locally_stable"
    if derivative_value > tolerance:
        return "locally_unstable"
    return "inconclusive_by_linearization"

def build_stability_records() -> list[StabilityRecord]:
    records: list[StabilityRecord] = []
    for eq in [0.0, 100.0]:
        derivative_value = logistic_derivative(eq, growth_rate=0.6, carrying_capacity=100.0)
        records.append(StabilityRecord(
            scenario="logistic_growth",
            equilibrium=eq,
            derivative_value=derivative_value,
            stability=classify_scalar_stability(derivative_value),
            domain_min=0.0,
            domain_max=100.0,
            warning="Logistic stability assumes fixed carrying capacity and smooth density limitation."
        ))

    threshold = 0.4
    for eq in [0.0, threshold, 1.0]:
        derivative_value = numerical_derivative(lambda x: bistable_rate(x, threshold), eq)
        records.append(StabilityRecord(
            scenario="bistable_threshold",
            equilibrium=eq,
            derivative_value=derivative_value,
            stability=classify_scalar_stability(derivative_value),
            domain_min=0.0,
            domain_max=1.0,
            warning="Threshold stability depends on the assumed threshold and domain."
        ))
    return records

def write_outputs(output_dir: Path, records: list[StabilityRecord]) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]
    with (output_dir / "tables" / "equilibrium_stability_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "equilibrium_stability_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    records = build_stability_records()
    write_outputs(args.output_dir, records)
    print("Equilibrium and stability audit complete.")

if __name__ == "__main__":
    main()
