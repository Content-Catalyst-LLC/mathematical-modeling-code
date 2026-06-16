from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class ODESolverRecord:
    step: int
    time: float
    solver_value: float
    exact_value: float
    absolute_error: float
    solver_method: str
    step_size: float
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

def tolerance_threshold(atol: float, rtol: float, state_value: float) -> float:
    if atol < 0 or rtol < 0:
        raise ValueError("tolerances must be nonnegative")
    return atol + rtol * abs(state_value)

def stiffness_indicator(fast_rate: float, slow_rate: float) -> float:
    if slow_rate == 0:
        raise ValueError("slow_rate must be nonzero")
    return abs(fast_rate / slow_rate)

def solver_audit(y0: float, decay_rate: float, step_size: float, stop_time: float) -> list[ODESolverRecord]:
    if step_size <= 0:
        raise ValueError("step_size must be positive")
    steps = int(round(stop_time / step_size))
    y = y0
    records: list[ODESolverRecord] = []

    for step in range(steps + 1):
        t = step * step_size
        exact = exact_solution(t, y0, decay_rate)
        records.append(ODESolverRecord(
            step=step,
            time=t,
            solver_value=y,
            exact_value=exact,
            absolute_error=abs(y - exact),
            solver_method="fixed_step_rk4",
            step_size=step_size,
            warning="ODE solver outputs depend on equation, initial condition, method, tolerances, step size, stiffness, and diagnostics."
        ))
        y = rk4_step(t, y, step_size, decay_rate)
    return records

def step_size_comparison(y0: float, decay_rate: float, stop_time: float) -> list[dict]:
    rows = []
    for h in [1.0, 0.5, 0.25, 0.1]:
        records = solver_audit(y0, decay_rate, h, stop_time)
        rows.append({
            "step_size": h,
            "records": len(records),
            "solver_method": "fixed_step_rk4",
            "final_absolute_error": records[-1].absolute_error,
            "final_solver_value": records[-1].solver_value,
            "final_exact_value": records[-1].exact_value
        })
    return rows

def write_outputs(output_dir: Path, records: list[ODESolverRecord], summary: dict, comparison: list[dict]) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]
    with (output_dir / "tables" / "ode_solver_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    with (output_dir / "tables" / "ode_solver_step_size_comparison.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(comparison[0].keys()))
        writer.writeheader()
        writer.writerows(comparison)
    (output_dir / "json" / "ode_solver_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    (output_dir / "json" / "ode_solver_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    (output_dir / "json" / "ode_solver_step_size_comparison.json").write_text(json.dumps(comparison, indent=2, sort_keys=True), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--y0", type=float, default=100.0)
    parser.add_argument("--decay-rate", type=float, default=0.35)
    parser.add_argument("--step-size", type=float, default=0.5)
    parser.add_argument("--stop-time", type=float, default=20.0)
    parser.add_argument("--atol", type=float, default=1e-8)
    parser.add_argument("--rtol", type=float, default=1e-6)
    args = parser.parse_args()

    records = solver_audit(args.y0, args.decay_rate, args.step_size, args.stop_time)
    comparison = step_size_comparison(args.y0, args.decay_rate, args.stop_time)
    summary = {
        "initial_value": args.y0,
        "decay_rate": args.decay_rate,
        "step_size": args.step_size,
        "stop_time": args.stop_time,
        "solver_method": "fixed_step_rk4",
        "absolute_tolerance": args.atol,
        "relative_tolerance": args.rtol,
        "records": len(records),
        "final_absolute_error": records[-1].absolute_error,
        "final_tolerance_threshold": tolerance_threshold(args.atol, args.rtol, records[-1].solver_value),
        "interpretation": "The workflow records solver method, step size, tolerance settings, benchmark error, and interpretation warning."
    }
    write_outputs(args.output_dir, records, summary, comparison)
    print("ODE solver workflow audit complete.")

if __name__ == "__main__":
    main()
