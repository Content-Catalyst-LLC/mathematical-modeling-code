from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class ConvergenceRecord:
    step_size: float
    steps: int
    solver_method: str
    final_numeric_value: float
    final_exact_value: float
    final_absolute_error: float
    error_ratio_to_previous: str
    warning: str

def rate_function(t: float, y: float, decay_rate: float) -> float:
    return -decay_rate * y

def exact_solution(t: float, y0: float, decay_rate: float) -> float:
    return y0 * math.exp(-decay_rate * t)

def rk4_step(t: float, y: float, h: float, decay_rate: float) -> float:
    k1 = rate_function(t, y, decay_rate)
    k2 = rate_function(t + h / 2.0, y + h * k1 / 2.0, decay_rate)
    k3 = rate_function(t + h / 2.0, y + h * k2 / 2.0, decay_rate)
    k4 = rate_function(t + h, y + h * k3, decay_rate)
    return y + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

def simulate(y0: float, decay_rate: float, h: float, stop_time: float) -> float:
    if h <= 0:
        raise ValueError("step size must be positive")
    steps = int(round(stop_time / h))
    y = y0
    for step in range(steps):
        t = step * h
        y = rk4_step(t, y, h, decay_rate)
    return y

def convergence_audit(y0: float = 100.0, decay_rate: float = 0.35, stop_time: float = 20.0) -> list[ConvergenceRecord]:
    exact_final = exact_solution(stop_time, y0, decay_rate)
    step_sizes = [1.0, 0.5, 0.25, 0.125]
    previous_error = None
    records: list[ConvergenceRecord] = []
    for h in step_sizes:
        numeric = simulate(y0, decay_rate, h, stop_time)
        error = abs(numeric - exact_final)
        ratio = "not_applicable" if previous_error is None or error == 0 else f"{previous_error / error:.4f}"
        records.append(ConvergenceRecord(
            step_size=h,
            steps=int(round(stop_time / h)),
            solver_method="fixed_step_rk4",
            final_numeric_value=numeric,
            final_exact_value=exact_final,
            final_absolute_error=error,
            error_ratio_to_previous=ratio,
            warning="Convergence evidence supports numerical reliability, not empirical validity."
        ))
        previous_error = error
    return records

def stability_amplification_factor(step_size: float, eigenvalue: float) -> float:
    return abs(1.0 + step_size * eigenvalue)

def write_outputs(output_dir: Path, records: list[ConvergenceRecord]) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]

    with (output_dir / "tables" / "convergence_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "convergence_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report_lines = [
        "# Error and Convergence Audit",
        "",
        "| Step size | Steps | Final absolute error | Error ratio to previous |",
        "|---:|---:|---:|---:|",
    ]
    for record in records:
        report_lines.append(f"| {record.step_size} | {record.steps} | {record.final_absolute_error:.12e} | {record.error_ratio_to_previous} |")
    report_lines.append("")
    report_lines.append("Convergence evidence should be interpreted as numerical evidence, not empirical proof.")
    (output_dir / "reports" / "convergence_audit.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    records = convergence_audit()
    write_outputs(args.output_dir, records)
    print("Stability, error, and convergence audit outputs generated.")

if __name__ == "__main__":
    main()
