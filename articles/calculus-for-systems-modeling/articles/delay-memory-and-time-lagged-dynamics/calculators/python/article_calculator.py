#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "outputs"

@dataclass
class CalculatorResult:
    calculator: str
    inputs: dict
    result: dict
    interpretation: str
    warning: str = ""

def ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def write_outputs(name: str, payload: CalculatorResult) -> None:
    ensure_output_dir()
    (OUTPUT_DIR / f"{name}.json").write_text(json.dumps(asdict(payload), indent=2, sort_keys=True), encoding="utf-8")
    flat = {"calculator": payload.calculator, "interpretation": payload.interpretation, "warning": payload.warning}
    flat.update({f"input_{k}": v for k, v in payload.inputs.items() if not isinstance(v, list)})
    flat.update({f"result_{k}": v for k, v in payload.result.items() if not isinstance(v, (list, dict))})
    with (OUTPUT_DIR / f"{name}.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(flat.keys()))
        writer.writeheader()
        writer.writerow(flat)

def write_series(name: str, rows: list[dict]) -> None:
    ensure_output_dir()
    (OUTPUT_DIR / f"{name}.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    with (OUTPUT_DIR / f"{name}.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

def delay_steps(delay: float, dt: float) -> int:
    if dt <= 0:
        raise ValueError("dt must be positive")
    return round(delay / dt)

def memory_kernel(age: float, decay_rate: float) -> float:
    return math.exp(-decay_rate * age)

def delayed_adjustment_rows(initial_state: float, target: float, adjustment_rate: float, delay: float, dt: float, steps: int) -> list[dict]:
    dsteps = delay_steps(delay, dt)
    states = [initial_state]
    rows = []
    for step in range(steps + 1):
        time = step * dt
        current = states[-1]
        delayed_index = step - dsteps
        delayed = initial_state if delayed_index < 0 else states[delayed_index]
        derivative = adjustment_rate * (target - delayed)
        rows.append({"step": step, "time": time, "current_state": current, "delayed_state": delayed, "derivative_value": derivative, "target": target, "absolute_gap": abs(current - target)})
        states.append(current + dt * derivative)
    return rows

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("delay-steps")
    p.add_argument("--delay", type=float, default=5.0)
    p.add_argument("--dt", type=float, default=0.1)

    p = sub.add_parser("delayed-lookup")
    p.add_argument("--initial-state", type=float, default=80.0)
    p.add_argument("--delay-steps", type=int, default=50)
    p.add_argument("--step", type=int, default=10)

    p = sub.add_parser("memory-kernel")
    p.add_argument("--age", type=float, default=3.0)
    p.add_argument("--decay-rate", type=float, default=0.4)

    p = sub.add_parser("delayed-adjustment")
    p.add_argument("--initial-state", type=float, default=80.0)
    p.add_argument("--target", type=float, default=100.0)
    p.add_argument("--adjustment-rate", type=float, default=0.2)
    p.add_argument("--delay", type=float, default=5.0)
    p.add_argument("--dt", type=float, default=0.1)
    p.add_argument("--steps", type=int, default=300)

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "delay-steps":
        value = delay_steps(args.delay, args.dt)
        emit(cmd, args, {"delay_steps": value}, "Converts continuous delay into discrete simulation steps.", "This assumes the delay aligns with or is rounded to the time step.")
    elif cmd == "delayed-lookup":
        delayed_index = args.step - args.delay_steps
        value = args.initial_state if delayed_index < 0 else None
        emit(cmd, args, {"delayed_index": delayed_index, "uses_history": delayed_index < 0, "lookup_value_if_history": value}, "Checks whether a delayed lookup uses pre-simulation history.", "History assumptions should be documented.")
    elif cmd == "memory-kernel":
        value = memory_kernel(args.age, args.decay_rate)
        emit(cmd, args, {"kernel_weight": value}, "Computes an exponential memory-kernel weight.", "Kernel shape should be justified and sensitivity tested.")
    elif cmd == "delayed-adjustment":
        rows = delayed_adjustment_rows(args.initial_state, args.target, args.adjustment_rate, args.delay, args.dt, args.steps)
        write_series("delayed_adjustment", rows)
        emit(cmd, args, {"records": len(rows), "max_gap": max(row["absolute_gap"] for row in rows), "final_gap": rows[-1]["absolute_gap"]}, "Runs a delayed adjustment simulation.", "Delayed feedback can generate overshoot or oscillation depending on timing and strength.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
