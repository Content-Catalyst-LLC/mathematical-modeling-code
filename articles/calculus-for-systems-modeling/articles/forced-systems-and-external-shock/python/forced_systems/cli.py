from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class ShockRecord:
    step: int
    time: float
    baseline_state: float
    forced_state: float
    shock_value: float
    absolute_deviation: float
    warning: str

def restoring_rate(x: float, equilibrium: float, recovery_rate: float) -> float:
    return -recovery_rate * (x - equilibrium)

def impulse_shock(time: float, shock_time: float, shock_magnitude: float, tolerance: float = 1e-12) -> float:
    return shock_magnitude if abs(time - shock_time) < tolerance else 0.0

def step_forcing(time: float, start_time: float, level: float) -> float:
    return level if time >= start_time else 0.0

def periodic_forcing(time: float, amplitude: float, angular_frequency: float, phase: float = 0.0) -> float:
    return amplitude * math.sin(angular_frequency * time + phase)

def simulate_forced_system(
    initial_state: float,
    equilibrium: float,
    recovery_rate: float,
    shock_time: float,
    shock_magnitude: float,
    dt: float,
    steps: int
) -> list[ShockRecord]:
    records: list[ShockRecord] = []
    baseline = initial_state
    forced = initial_state
    for step in range(steps + 1):
        time = step * dt
        shock_value = impulse_shock(time, shock_time, shock_magnitude)
        records.append(ShockRecord(
            step=step,
            time=time,
            baseline_state=baseline,
            forced_state=forced,
            shock_value=shock_value,
            absolute_deviation=abs(forced - baseline),
            warning="Shock response depends on forcing form, timing, magnitude, recovery rate, and numerical step size."
        ))
        baseline = baseline + dt * restoring_rate(baseline, equilibrium, recovery_rate)
        if shock_value != 0:
            forced = forced + shock_value
        forced = forced + dt * restoring_rate(forced, equilibrium, recovery_rate)
    return records

def shock_summary(records: list[ShockRecord], dt: float, shock_time: float, shock_magnitude: float, recovery_rate: float) -> dict:
    deviations = [record.absolute_deviation for record in records]
    max_deviation = max(deviations)
    cumulative_deviation = sum(deviations) * dt
    recovery_threshold = max_deviation * 0.05 if max_deviation > 0 else 0.0
    recovery_time = None
    shock_seen = False
    for record in records:
        if record.time >= shock_time:
            shock_seen = True
        if shock_seen and record.absolute_deviation <= recovery_threshold:
            recovery_time = record.time
            break
    return {
        "max_deviation": max_deviation,
        "cumulative_deviation": cumulative_deviation,
        "shock_time": shock_time,
        "shock_magnitude": shock_magnitude,
        "recovery_rate": recovery_rate,
        "recovery_threshold": recovery_threshold,
        "first_recovery_time": recovery_time,
        "interpretation": "The same shock magnitude can produce different recovery paths under different internal dynamics."
    }

def write_outputs(output_dir: Path, records: list[ShockRecord], summary: dict) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]
    with (output_dir / "tables" / "forced_system_shock_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "forced_system_shock_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    (output_dir / "json" / "shock_response_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    with (output_dir / "tables" / "shock_response_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary.keys()))
        writer.writeheader()
        writer.writerow(summary)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--initial-state", type=float, default=100.0)
    parser.add_argument("--equilibrium", type=float, default=100.0)
    parser.add_argument("--recovery-rate", type=float, default=0.15)
    parser.add_argument("--shock-time", type=float, default=10.0)
    parser.add_argument("--shock-magnitude", type=float, default=-30.0)
    parser.add_argument("--dt", type=float, default=0.1)
    parser.add_argument("--steps", type=int, default=300)
    args = parser.parse_args()
    records = simulate_forced_system(
        args.initial_state,
        args.equilibrium,
        args.recovery_rate,
        args.shock_time,
        args.shock_magnitude,
        args.dt,
        args.steps,
    )
    summary = shock_summary(records, args.dt, args.shock_time, args.shock_magnitude, args.recovery_rate)
    write_outputs(args.output_dir, records, summary)
    print("Forced-system shock audit complete.")

if __name__ == "__main__":
    main()
