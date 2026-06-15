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

def forcing_function(t: float, amplitude: float, frequency: float) -> float:
    return amplitude * math.cos(frequency * t)

def oscillator_acceleration(position: float, velocity: float, time: float, damping_ratio: float, natural_frequency: float, forcing_amplitude: float, forcing_frequency: float) -> float:
    return forcing_function(time, forcing_amplitude, forcing_frequency) - 2.0*damping_ratio*natural_frequency*velocity - natural_frequency*natural_frequency*position

def damping_classification(zeta: float) -> str:
    if zeta == 0:
        return "undamped"
    if 0 < zeta < 1:
        return "underdamped"
    if zeta == 1:
        return "critically_damped"
    return "overdamped"

def period_from_natural_frequency(natural_frequency: float) -> float:
    return 2.0 * math.pi / natural_frequency

def euler_step(position: float, velocity: float, dt: float, damping_ratio: float, natural_frequency: float, forcing_amplitude: float, forcing_frequency: float, time: float = 0.0) -> dict:
    a = oscillator_acceleration(position, velocity, time, damping_ratio, natural_frequency, forcing_amplitude, forcing_frequency)
    next_velocity = velocity + dt*a
    next_position = position + dt*next_velocity
    return {"next_position": next_position, "next_velocity": next_velocity, "acceleration": a}

def simulate(position: float, velocity: float, damping_ratio: float, natural_frequency: float, forcing_amplitude: float, forcing_frequency: float, dt: float, steps: int) -> list[dict]:
    rows = []
    x = position
    v = velocity
    for n in range(steps + 1):
        t = n*dt
        a = oscillator_acceleration(x, v, t, damping_ratio, natural_frequency, forcing_amplitude, forcing_frequency)
        rows.append({"step": n, "time": t, "position": x, "velocity": v, "acceleration": a, "forcing": forcing_function(t, forcing_amplitude, forcing_frequency)})
        v = v + dt*a
        x = x + dt*v
    return rows

def write_series(name: str, rows: list[dict]) -> None:
    ensure_output_dir()
    (OUTPUT_DIR / f"{name}_series.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    with (OUTPUT_DIR / f"{name}_series.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("damping-classification")
    p.add_argument("--damping-ratio", type=float, default=0.2)

    p = sub.add_parser("period")
    p.add_argument("--natural-frequency", type=float, default=1.0)

    p = sub.add_parser("acceleration")
    p.add_argument("--position", type=float, default=1.0)
    p.add_argument("--velocity", type=float, default=0.0)
    p.add_argument("--time", type=float, default=0.0)
    p.add_argument("--damping-ratio", type=float, default=0.2)
    p.add_argument("--natural-frequency", type=float, default=1.0)
    p.add_argument("--forcing-amplitude", type=float, default=0.0)
    p.add_argument("--forcing-frequency", type=float, default=1.0)

    p = sub.add_parser("euler-step")
    p.add_argument("--position", type=float, default=1.0)
    p.add_argument("--velocity", type=float, default=0.0)
    p.add_argument("--dt", type=float, default=0.02)
    p.add_argument("--damping-ratio", type=float, default=0.2)
    p.add_argument("--natural-frequency", type=float, default=1.0)
    p.add_argument("--forcing-amplitude", type=float, default=0.0)
    p.add_argument("--forcing-frequency", type=float, default=1.0)

    p = sub.add_parser("simulate-oscillator")
    p.add_argument("--scenario", default="underdamped")
    p.add_argument("--position", type=float, default=1.0)
    p.add_argument("--velocity", type=float, default=0.0)
    p.add_argument("--damping-ratio", type=float, default=0.2)
    p.add_argument("--natural-frequency", type=float, default=1.0)
    p.add_argument("--forcing-amplitude", type=float, default=0.0)
    p.add_argument("--forcing-frequency", type=float, default=1.0)
    p.add_argument("--dt", type=float, default=0.02)
    p.add_argument("--steps", type=int, default=50)

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "damping-classification":
        cls = damping_classification(args.damping_ratio)
        emit(cmd, args, {"classification": cls}, "Classifies oscillator damping regime.", "Damping classification depends on normalized model form.")
    elif cmd == "period":
        period = period_from_natural_frequency(args.natural_frequency)
        emit(cmd, args, {"period": period}, "Computes T = 2*pi/omega.", "Period assumes the stated natural frequency is valid.")
    elif cmd == "acceleration":
        a = oscillator_acceleration(args.position, args.velocity, args.time, args.damping_ratio, args.natural_frequency, args.forcing_amplitude, args.forcing_frequency)
        emit(cmd, args, {"acceleration": a, "forcing": forcing_function(args.time, args.forcing_amplitude, args.forcing_frequency)}, "Computes second-order oscillator acceleration.", "Acceleration combines forcing, damping, and restoring terms.")
    elif cmd == "euler-step":
        result = euler_step(args.position, args.velocity, args.dt, args.damping_ratio, args.natural_frequency, args.forcing_amplitude, args.forcing_frequency)
        emit(cmd, args, result, "Computes one explicit Euler step for position and velocity.", "Euler error depends on step size.")
    elif cmd == "simulate-oscillator":
        rows = simulate(args.position, args.velocity, args.damping_ratio, args.natural_frequency, args.forcing_amplitude, args.forcing_frequency, args.dt, args.steps)
        write_series(f"simulate_oscillator_{args.scenario}", rows)
        emit(cmd, args, {"records": len(rows), "final_position": rows[-1]["position"], "final_velocity": rows[-1]["velocity"]}, "Simulates a second-order oscillator as a first-order system.", "Check solver sensitivity before interpreting oscillation.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
