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

def restoring_rate(x: float, equilibrium: float, recovery_rate: float) -> float:
    return -recovery_rate * (x - equilibrium)

def impulse_shock(time: float, shock_time: float, shock_magnitude: float, tolerance: float = 1e-12) -> float:
    return shock_magnitude if abs(time - shock_time) < tolerance else 0.0

def step_forcing(time: float, start_time: float, level: float) -> float:
    return level if time >= start_time else 0.0

def periodic_forcing(time: float, amplitude: float, angular_frequency: float, phase: float = 0.0) -> float:
    return amplitude * math.sin(angular_frequency * time + phase)

def forced_recovery_rows(initial_state: float, equilibrium: float, recovery_rate: float, shock_time: float, shock_magnitude: float, dt: float, steps: int) -> list[dict]:
    rows = []
    baseline = initial_state
    forced = initial_state
    for step in range(steps + 1):
        time = step * dt
        shock_value = impulse_shock(time, shock_time, shock_magnitude)
        rows.append({"step": step, "time": time, "baseline_state": baseline, "forced_state": forced, "shock_value": shock_value, "absolute_deviation": abs(forced - baseline)})
        baseline = baseline + dt * restoring_rate(baseline, equilibrium, recovery_rate)
        if shock_value != 0:
            forced += shock_value
        forced = forced + dt * restoring_rate(forced, equilibrium, recovery_rate)
    return rows

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("impulse-shock")
    p.add_argument("--time", type=float, default=10.0)
    p.add_argument("--shock-time", type=float, default=10.0)
    p.add_argument("--shock-magnitude", type=float, default=-30.0)

    p = sub.add_parser("step-forcing")
    p.add_argument("--time", type=float, default=12.0)
    p.add_argument("--start-time", type=float, default=10.0)
    p.add_argument("--level", type=float, default=5.0)

    p = sub.add_parser("periodic-forcing")
    p.add_argument("--time", type=float, default=1.57079632679)
    p.add_argument("--amplitude", type=float, default=2.0)
    p.add_argument("--angular-frequency", type=float, default=1.0)
    p.add_argument("--phase", type=float, default=0.0)

    p = sub.add_parser("forced-recovery")
    p.add_argument("--initial-state", type=float, default=100.0)
    p.add_argument("--equilibrium", type=float, default=100.0)
    p.add_argument("--recovery-rate", type=float, default=0.15)
    p.add_argument("--shock-time", type=float, default=10.0)
    p.add_argument("--shock-magnitude", type=float, default=-30.0)
    p.add_argument("--dt", type=float, default=0.1)
    p.add_argument("--steps", type=int, default=300)

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "impulse-shock":
        value = impulse_shock(args.time, args.shock_time, args.shock_magnitude)
        emit(cmd, args, {"shock_value": value}, "Computes an impulse-shock value at one time.", "Impulse shocks require time-scale and magnitude justification.")
    elif cmd == "step-forcing":
        value = step_forcing(args.time, args.start_time, args.level)
        emit(cmd, args, {"forcing_value": value}, "Computes a step-forcing value at one time.", "Step forcing represents a persistent shift, not a temporary event.")
    elif cmd == "periodic-forcing":
        value = periodic_forcing(args.time, args.amplitude, args.angular_frequency, args.phase)
        emit(cmd, args, {"forcing_value": value}, "Computes periodic forcing at one time.", "Amplitude, frequency, and phase should be documented.")
    elif cmd == "forced-recovery":
        rows = forced_recovery_rows(args.initial_state, args.equilibrium, args.recovery_rate, args.shock_time, args.shock_magnitude, args.dt, args.steps)
        write_series("forced_recovery", rows)
        max_deviation = max(row["absolute_deviation"] for row in rows)
        cumulative_deviation = sum(row["absolute_deviation"] for row in rows) * args.dt
        emit(cmd, args, {"records": len(rows), "max_deviation": max_deviation, "cumulative_deviation": cumulative_deviation}, "Runs a baseline-versus-shocked recovery simulation.", "Shock response depends on forcing form, timing, magnitude, recovery rate, and step size.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
