from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class EulerRecord:
    step: int
    time: float
    euler_value: float
    exact_value: float
    absolute_error: float
    step_size: float
    stability_multiplier: float
    stability_status: str
    warning: str

def rate_function(t: float, y: float, decay_rate: float) -> float:
    return -decay_rate * y

def exact_solution(t: float, y0: float, decay_rate: float) -> float:
    return y0 * math.exp(-decay_rate * t)

def euler_step(t: float, y: float, h: float, decay_rate: float) -> float:
    return y + h * rate_function(t, y, decay_rate)

def stability_multiplier(step_size: float, decay_rate: float) -> float:
    return 1.0 - step_size * decay_rate

def stability_status(step_size: float, decay_rate: float) -> str:
    multiplier = stability_multiplier(step_size, decay_rate)
    return "stable_for_simple_decay" if abs(multiplier) <= 1.0 else "unstable_risk"

def euler_audit(y0: float, decay_rate: float, step_size: float, stop_time: float) -> list[EulerRecord]:
    if step_size <= 0:
        raise ValueError("step_size must be positive")
    steps = int(round(stop_time / step_size))
    y = y0
    multiplier = stability_multiplier(step_size, decay_rate)
    status = stability_status(step_size, decay_rate)
    records: list[EulerRecord] = []

    for step in range(steps + 1):
        t = step * step_size
        exact = exact_solution(t, y0, decay_rate)
        records.append(EulerRecord(
            step=step,
            time=t,
            euler_value=y,
            exact_value=exact,
            absolute_error=abs(y - exact),
            step_size=step_size,
            stability_multiplier=multiplier,
            stability_status=status,
            warning="Euler estimates depend on time step, rate function, initial condition, stability, and accumulated error."
        ))
        y = euler_step(t, y, step_size, decay_rate)
    return records

def logistic_step(y: float, r: float, carrying_capacity: float, h: float) -> float:
    return y + h * r * y * (1.0 - y / carrying_capacity)

def write_outputs(output_dir: Path, records: list[EulerRecord], summary: dict) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]
    with (output_dir / "tables" / "euler_method_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "euler_method_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    (output_dir / "json" / "euler_method_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    with (output_dir / "tables" / "euler_method_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary.keys()))
        writer.writeheader()
        writer.writerow(summary)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--y0", type=float, default=100.0)
    parser.add_argument("--decay-rate", type=float, default=0.35)
    parser.add_argument("--step-size", type=float, default=0.1)
    parser.add_argument("--stop-time", type=float, default=20.0)
    args = parser.parse_args()

    records = euler_audit(args.y0, args.decay_rate, args.step_size, args.stop_time)
    summary = {
        "initial_value": args.y0,
        "decay_rate": args.decay_rate,
        "step_size": args.step_size,
        "stop_time": args.stop_time,
        "records": len(records),
        "final_euler_value": records[-1].euler_value,
        "final_exact_value": records[-1].exact_value,
        "final_absolute_error": records[-1].absolute_error,
        "stability_multiplier": records[0].stability_multiplier,
        "stability_status": records[0].stability_status,
        "interpretation": "Euler's Method approximates the decay trajectory, but error and stability depend on the time step."
    }
    write_outputs(args.output_dir, records, summary)
    print("Euler method audit complete.")

if __name__ == "__main__":
    main()
