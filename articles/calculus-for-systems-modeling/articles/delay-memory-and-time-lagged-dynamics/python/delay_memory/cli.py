from __future__ import annotations
import argparse, csv, json
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class DelayRecord:
    step: int
    time: float
    current_state: float
    delayed_state: float
    derivative_value: float
    target: float
    absolute_gap: float
    warning: str

def history_function(time: float, initial_value: float) -> float:
    return initial_value

def delay_steps(delay: float, dt: float) -> int:
    if dt <= 0:
        raise ValueError("dt must be positive")
    if delay < 0:
        raise ValueError("delay must be nonnegative")
    return round(delay / dt)

def delayed_lookup(states: list[float], step: int, delay_steps_value: int, initial_value: float) -> float:
    delayed_index = step - delay_steps_value
    if delayed_index < 0:
        return history_function(0.0, initial_value)
    return states[delayed_index]

def memory_kernel_exponential(age: float, decay_rate: float) -> float:
    import math
    if age < 0:
        raise ValueError("age must be nonnegative")
    if decay_rate < 0:
        raise ValueError("decay_rate must be nonnegative")
    return math.exp(-decay_rate * age)

def simulate_delayed_adjustment(
    initial_state: float,
    target: float,
    adjustment_rate: float,
    delay: float,
    dt: float,
    steps: int
) -> list[DelayRecord]:
    delay_steps_value = delay_steps(delay, dt)
    states = [initial_state]
    records: list[DelayRecord] = []

    for step in range(steps + 1):
        time = step * dt
        current_state = states[-1]
        delayed_state = delayed_lookup(states, step, delay_steps_value, initial_state)
        derivative_value = adjustment_rate * (target - delayed_state)

        records.append(DelayRecord(
            step=step,
            time=time,
            current_state=current_state,
            delayed_state=delayed_state,
            derivative_value=derivative_value,
            target=target,
            absolute_gap=abs(current_state - target),
            warning="Delayed adjustment depends on delay length, history function, time step, and feedback strength."
        ))

        states.append(current_state + dt * derivative_value)

    return records

def write_outputs(output_dir: Path, records: list[DelayRecord], summary: dict) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]
    with (output_dir / "tables" / "delay_memory_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "delay_memory_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    (output_dir / "json" / "delay_memory_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    with (output_dir / "tables" / "delay_memory_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary.keys()))
        writer.writeheader()
        writer.writerow(summary)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--initial-state", type=float, default=80.0)
    parser.add_argument("--target", type=float, default=100.0)
    parser.add_argument("--adjustment-rate", type=float, default=0.2)
    parser.add_argument("--delay", type=float, default=5.0)
    parser.add_argument("--dt", type=float, default=0.1)
    parser.add_argument("--steps", type=int, default=300)
    args = parser.parse_args()

    records = simulate_delayed_adjustment(
        initial_state=args.initial_state,
        target=args.target,
        adjustment_rate=args.adjustment_rate,
        delay=args.delay,
        dt=args.dt,
        steps=args.steps,
    )

    summary = {
        "initial_state": args.initial_state,
        "target": args.target,
        "adjustment_rate": args.adjustment_rate,
        "delay": args.delay,
        "dt": args.dt,
        "delay_steps": delay_steps(args.delay, args.dt),
        "max_gap": max(record.absolute_gap for record in records),
        "final_gap": records[-1].absolute_gap,
        "interpretation": "Delayed adjustment can generate overshoot or oscillation when feedback responds to old information."
    }

    write_outputs(args.output_dir, records, summary)
    print("Delay and memory audit complete.")

if __name__ == "__main__":
    main()
