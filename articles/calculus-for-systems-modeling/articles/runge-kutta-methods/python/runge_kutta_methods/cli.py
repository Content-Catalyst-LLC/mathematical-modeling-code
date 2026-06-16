from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class RungeKuttaRecord:
    step: int
    time: float
    euler_value: float
    rk4_value: float
    exact_value: float
    euler_absolute_error: float
    rk4_absolute_error: float
    step_size: float
    warning: str

def rate_function(t: float, y: float, decay_rate: float) -> float:
    return -decay_rate * y

def exact_solution(t: float, y0: float, decay_rate: float) -> float:
    return y0 * math.exp(-decay_rate * t)

def euler_step(t: float, y: float, h: float, decay_rate: float) -> float:
    return y + h * rate_function(t, y, decay_rate)

def midpoint_step(t: float, y: float, h: float, decay_rate: float) -> float:
    k1 = rate_function(t, y, decay_rate)
    k2 = rate_function(t + h / 2.0, y + h * k1 / 2.0, decay_rate)
    return y + h * k2

def heun_step(t: float, y: float, h: float, decay_rate: float) -> float:
    k1 = rate_function(t, y, decay_rate)
    k2 = rate_function(t + h, y + h * k1, decay_rate)
    return y + h * 0.5 * (k1 + k2)

def rk4_step(t: float, y: float, h: float, decay_rate: float) -> float:
    k1 = rate_function(t, y, decay_rate)
    k2 = rate_function(t + h / 2.0, y + h * k1 / 2.0, decay_rate)
    k3 = rate_function(t + h / 2.0, y + h * k2 / 2.0, decay_rate)
    k4 = rate_function(t + h, y + h * k3, decay_rate)
    return y + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

def rk4_stage_values(t: float, y: float, h: float, decay_rate: float) -> dict[str, float]:
    k1 = rate_function(t, y, decay_rate)
    k2 = rate_function(t + h / 2.0, y + h * k1 / 2.0, decay_rate)
    k3 = rate_function(t + h / 2.0, y + h * k2 / 2.0, decay_rate)
    k4 = rate_function(t + h, y + h * k3, decay_rate)
    return {"k1": k1, "k2": k2, "k3": k3, "k4": k4}

def rk_audit(y0: float, decay_rate: float, step_size: float, stop_time: float) -> list[RungeKuttaRecord]:
    if step_size <= 0:
        raise ValueError("step_size must be positive")
    steps = int(round(stop_time / step_size))
    y_euler = y0
    y_rk4 = y0
    records: list[RungeKuttaRecord] = []

    for step in range(steps + 1):
        t = step * step_size
        exact = exact_solution(t, y0, decay_rate)
        records.append(RungeKuttaRecord(
            step=step,
            time=t,
            euler_value=y_euler,
            rk4_value=y_rk4,
            exact_value=exact,
            euler_absolute_error=abs(y_euler - exact),
            rk4_absolute_error=abs(y_rk4 - exact),
            step_size=step_size,
            warning="Runge–Kutta estimates depend on rate function, step size, smoothness, stiffness, and benchmark comparison."
        ))
        y_euler = euler_step(t, y_euler, step_size, decay_rate)
        y_rk4 = rk4_step(t, y_rk4, step_size, decay_rate)
    return records

def write_outputs(output_dir: Path, records: list[RungeKuttaRecord], summary: dict) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]
    with (output_dir / "tables" / "runge_kutta_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "runge_kutta_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    (output_dir / "json" / "runge_kutta_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    with (output_dir / "tables" / "runge_kutta_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary.keys()))
        writer.writeheader()
        writer.writerow(summary)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--y0", type=float, default=100.0)
    parser.add_argument("--decay-rate", type=float, default=0.35)
    parser.add_argument("--step-size", type=float, default=0.5)
    parser.add_argument("--stop-time", type=float, default=20.0)
    args = parser.parse_args()

    records = rk_audit(args.y0, args.decay_rate, args.step_size, args.stop_time)
    summary = {
        "initial_value": args.y0,
        "decay_rate": args.decay_rate,
        "step_size": args.step_size,
        "stop_time": args.stop_time,
        "records": len(records),
        "final_euler_error": records[-1].euler_absolute_error,
        "final_rk4_error": records[-1].rk4_absolute_error,
        "interpretation": "RK4 uses multiple slope estimates per step and is much more accurate than Euler for this smooth benchmark."
    }
    write_outputs(args.output_dir, records, summary)
    print("Runge-Kutta audit complete.")

if __name__ == "__main__":
    main()
