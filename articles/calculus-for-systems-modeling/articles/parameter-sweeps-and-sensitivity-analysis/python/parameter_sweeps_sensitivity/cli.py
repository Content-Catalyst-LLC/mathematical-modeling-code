from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class SweepRecord:
    growth_rate: float
    carrying_capacity: float
    initial_value: float
    stop_time: float
    final_value: float
    output_metric: str
    warning: str

@dataclass(frozen=True)
class SensitivityRecord:
    parameter: str
    baseline_value: float
    perturbation: float
    baseline_output: float
    forward_output: float
    backward_output: float
    finite_difference_sensitivity: float
    elasticity_estimate: float
    warning: str

def logistic_solution(t: float, x0: float, growth_rate: float, carrying_capacity: float) -> float:
    if x0 <= 0 or carrying_capacity <= 0:
        raise ValueError("x0 and carrying_capacity must be positive")
    return carrying_capacity / (1.0 + ((carrying_capacity - x0) / x0) * math.exp(-growth_rate * t))

def final_output(growth_rate: float, carrying_capacity: float, x0: float = 10.0, stop_time: float = 20.0) -> float:
    return logistic_solution(stop_time, x0, growth_rate, carrying_capacity)

def build_grid_sweep() -> list[SweepRecord]:
    growth_rates = [0.18, 0.25, 0.35, 0.45, 0.55]
    carrying_capacities = [80.0, 100.0, 125.0, 150.0]
    records: list[SweepRecord] = []
    for r in growth_rates:
        for k in carrying_capacities:
            records.append(SweepRecord(
                growth_rate=r,
                carrying_capacity=k,
                initial_value=10.0,
                stop_time=20.0,
                final_value=final_output(r, k),
                output_metric="final_state_value",
                warning="Sweep results depend on tested ranges, baseline assumptions, and model structure."
            ))
    return records

def finite_difference_sensitivity(parameter: str, baseline_r: float = 0.35, baseline_k: float = 100.0) -> SensitivityRecord:
    h = 0.01 if parameter == "growth_rate" else 1.0
    baseline = final_output(baseline_r, baseline_k)
    if parameter == "growth_rate":
        forward = final_output(baseline_r + h, baseline_k)
        backward = final_output(baseline_r - h, baseline_k)
        baseline_value = baseline_r
    elif parameter == "carrying_capacity":
        forward = final_output(baseline_r, baseline_k + h)
        backward = final_output(baseline_r, baseline_k - h)
        baseline_value = baseline_k
    else:
        raise ValueError("parameter must be growth_rate or carrying_capacity")
    sensitivity = (forward - backward) / (2.0 * h)
    elasticity = sensitivity * baseline_value / baseline
    return SensitivityRecord(
        parameter=parameter,
        baseline_value=baseline_value,
        perturbation=h,
        baseline_output=baseline,
        forward_output=forward,
        backward_output=backward,
        finite_difference_sensitivity=sensitivity,
        elasticity_estimate=elasticity,
        warning="Local sensitivity depends on baseline and perturbation size."
    )

def write_outputs(output_dir: Path) -> None:
    sweep_records = build_grid_sweep()
    sensitivity_records = [
        finite_difference_sensitivity("growth_rate"),
        finite_difference_sensitivity("carrying_capacity"),
    ]

    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)

    sweep_rows = [asdict(record) for record in sweep_records]
    sensitivity_rows = [asdict(record) for record in sensitivity_records]

    with (output_dir / "tables" / "parameter_sweep_grid.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(sweep_rows[0].keys()))
        writer.writeheader()
        writer.writerows(sweep_rows)

    with (output_dir / "tables" / "local_sensitivity_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(sensitivity_rows[0].keys()))
        writer.writeheader()
        writer.writerows(sensitivity_rows)

    (output_dir / "json" / "parameter_sweep_grid.json").write_text(json.dumps(sweep_rows, indent=2, sort_keys=True), encoding="utf-8")
    (output_dir / "json" / "local_sensitivity_audit.json").write_text(json.dumps(sensitivity_rows, indent=2, sort_keys=True), encoding="utf-8")

    report_lines = [
        "# Parameter Sweep and Sensitivity Audit",
        "",
        "This audit records a grid sweep and local finite-difference sensitivities for a logistic model.",
        "",
        "| Parameter | Baseline | Sensitivity | Elasticity |",
        "|---|---:|---:|---:|",
    ]
    for record in sensitivity_records:
        report_lines.append(f"| {record.parameter} | {record.baseline_value} | {record.finite_difference_sensitivity:.6f} | {record.elasticity_estimate:.6f} |")
    report_lines.append("")
    report_lines.append("Sensitivity evidence should be interpreted within tested ranges and documented assumptions.")
    (output_dir / "reports" / "parameter_sensitivity_audit.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Parameter sweep and sensitivity audit outputs generated.")

if __name__ == "__main__":
    main()
