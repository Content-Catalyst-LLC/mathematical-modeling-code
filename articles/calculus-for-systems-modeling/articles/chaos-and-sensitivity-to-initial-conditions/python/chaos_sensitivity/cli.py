from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class ChaosRecord:
    step: int
    x_reference: float
    x_perturbed: float
    absolute_difference: float
    log_difference: float | None
    warning: str

def logistic_map(x: float, r: float) -> float:
    return r * x * (1.0 - x)

def logistic_derivative(x: float, r: float) -> float:
    return r * (1.0 - 2.0 * x)

def simulate_pair(x0: float, perturbation: float, r: float, steps: int) -> list[ChaosRecord]:
    records: list[ChaosRecord] = []
    x_reference = x0
    x_perturbed = x0 + perturbation
    for step in range(steps + 1):
        difference = abs(x_reference - x_perturbed)
        log_difference = math.log(difference) if difference > 0 else None
        records.append(ChaosRecord(
            step=step,
            x_reference=x_reference,
            x_perturbed=x_perturbed,
            absolute_difference=difference,
            log_difference=log_difference,
            warning="Trajectory divergence depends on parameter value, initial uncertainty, numerical precision, and iteration count."
        ))
        x_reference = logistic_map(x_reference, r)
        x_perturbed = logistic_map(x_perturbed, r)
    return records

def estimate_lyapunov(x0: float, r: float, burn_in: int, sample_steps: int) -> float:
    x = x0
    for _ in range(burn_in):
        x = logistic_map(x, r)
    values: list[float] = []
    for _ in range(sample_steps):
        derivative_value = abs(logistic_derivative(x, r))
        if derivative_value > 0:
            values.append(math.log(derivative_value))
        x = logistic_map(x, r)
    return sum(values) / len(values)

def forecast_horizon(initial_uncertainty: float, acceptable_error: float, lyapunov_value: float) -> float | None:
    if initial_uncertainty <= 0 or acceptable_error <= 0 or lyapunov_value <= 0:
        return None
    return math.log(acceptable_error / initial_uncertainty) / lyapunov_value

def write_outputs(output_dir: Path, records: list[ChaosRecord], lyapunov_value: float) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]
    with (output_dir / "tables" / "chaos_sensitivity_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "chaos_sensitivity_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    summary = {
        "model": "logistic_map",
        "r": 3.9,
        "x0": 0.2,
        "burn_in": 100,
        "sample_steps": 1000,
        "lyapunov_estimate": lyapunov_value,
        "forecast_horizon_for_1e-8_to_1e-2": forecast_horizon(1e-8, 1e-2, lyapunov_value),
        "interpretation": "Positive values suggest sensitive dependence on initial conditions."
    }
    (output_dir / "json" / "lyapunov_estimate.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    with (output_dir / "tables" / "lyapunov_estimate.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary.keys()))
        writer.writeheader()
        writer.writerow(summary)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--x0", type=float, default=0.2)
    parser.add_argument("--perturbation", type=float, default=1e-8)
    parser.add_argument("--r", type=float, default=3.9)
    parser.add_argument("--steps", type=int, default=100)
    parser.add_argument("--burn-in", type=int, default=100)
    parser.add_argument("--sample-steps", type=int, default=1000)
    args = parser.parse_args()
    records = simulate_pair(args.x0, args.perturbation, args.r, args.steps)
    lyapunov_value = estimate_lyapunov(args.x0, args.r, args.burn_in, args.sample_steps)
    write_outputs(args.output_dir, records, lyapunov_value)
    print("Chaos sensitivity audit complete.")

if __name__ == "__main__":
    main()
