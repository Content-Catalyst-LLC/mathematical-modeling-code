from __future__ import annotations
import argparse, csv, json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable

@dataclass(frozen=True)
class NonlinearRecord:
    scenario: str
    time: float
    state: float
    rate: float
    parameter_a: float
    parameter_b: float
    parameter_c: float
    method: str
    warning: str

def logistic_rate(x: float, growth_rate: float, carrying_capacity: float) -> float:
    return growth_rate * x * (1.0 - x / carrying_capacity)

def bistable_rate(x: float, threshold: float) -> float:
    return x * (1.0 - x) * (x - threshold)

def logistic_equilibria(carrying_capacity: float) -> tuple[float, float]:
    return 0.0, carrying_capacity

def bistable_equilibria(threshold: float) -> tuple[float, float, float]:
    return 0.0, threshold, 1.0

def simulate_scalar(scenario: str, x0: float, dt: float, steps: int, rate_function: Callable[[float], float], parameters: tuple[float, float, float], warning: str) -> list[NonlinearRecord]:
    x = x0
    records: list[NonlinearRecord] = []
    for n in range(steps + 1):
        t = n * dt
        rate = rate_function(x)
        records.append(NonlinearRecord(
            scenario=scenario,
            time=t,
            state=x,
            rate=rate,
            parameter_a=parameters[0],
            parameter_b=parameters[1],
            parameter_c=parameters[2],
            method="explicit_euler",
            warning=warning
        ))
        x = x + dt * rate
    return records

def write_outputs(output_dir: Path, records: list[NonlinearRecord]) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]
    with (output_dir / "tables" / "nonlinear_dynamics_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "nonlinear_dynamics_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    equilibria = {
        "logistic_growth": logistic_equilibria(100.0),
        "bistable_threshold": bistable_equilibria(0.4)
    }
    (output_dir / "json" / "nonlinear_equilibria.json").write_text(json.dumps(equilibria, indent=2, sort_keys=True), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    logistic_records = simulate_scalar(
        "logistic_growth",
        10.0,
        0.05,
        300,
        lambda x: logistic_rate(x, growth_rate=0.6, carrying_capacity=100.0),
        (0.6, 100.0, 0.0),
        "Logistic growth assumes a fixed carrying capacity and smooth density limitation."
    )
    threshold_records = simulate_scalar(
        "bistable_threshold",
        0.35,
        0.05,
        300,
        lambda x: bistable_rate(x, threshold=0.4),
        (0.4, 0.0, 0.0),
        "Threshold behavior is illustrative and should not be interpreted without evidence for the threshold."
    )
    write_outputs(args.output_dir, logistic_records + threshold_records)
    print("Nonlinear dynamics audit complete.")

if __name__ == "__main__":
    main()
