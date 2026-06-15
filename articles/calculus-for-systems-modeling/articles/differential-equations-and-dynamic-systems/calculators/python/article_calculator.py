#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json
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

def exponential_rate(x: float, r: float) -> float:
    return r*x

def logistic_rate(x: float, r: float, capacity: float) -> float:
    return r*x*(1.0 - x/capacity)

def euler_step(x: float, rate: float, dt: float) -> float:
    return x + dt*rate

def simulate_exponential(x: float, r: float, dt: float, steps: int) -> list[dict]:
    rows = []
    for n in range(steps + 1):
        rate = exponential_rate(x, r)
        rows.append({"step": n, "time": n*dt, "state": x, "rate": rate})
        x = euler_step(x, rate, dt)
    return rows

def simulate_logistic(x: float, r: float, capacity: float, dt: float, steps: int) -> list[dict]:
    rows = []
    for n in range(steps + 1):
        rate = logistic_rate(x, r, capacity)
        rows.append({"step": n, "time": n*dt, "state": x, "rate": rate})
        x = euler_step(x, rate, dt)
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

    p = sub.add_parser("exponential-rate")
    p.add_argument("--state", type=float, default=10.0)
    p.add_argument("--growth-rate", type=float, default=0.35)

    p = sub.add_parser("logistic-rate")
    p.add_argument("--state", type=float, default=10.0)
    p.add_argument("--growth-rate", type=float, default=0.35)
    p.add_argument("--capacity", type=float, default=100.0)

    p = sub.add_parser("euler-step")
    p.add_argument("--state", type=float, default=10.0)
    p.add_argument("--rate", type=float, default=3.5)
    p.add_argument("--dt", type=float, default=0.1)

    p = sub.add_parser("simulate-exponential")
    p.add_argument("--state", type=float, default=10.0)
    p.add_argument("--growth-rate", type=float, default=0.35)
    p.add_argument("--dt", type=float, default=0.1)
    p.add_argument("--steps", type=int, default=20)

    p = sub.add_parser("simulate-logistic")
    p.add_argument("--state", type=float, default=10.0)
    p.add_argument("--growth-rate", type=float, default=0.35)
    p.add_argument("--capacity", type=float, default=100.0)
    p.add_argument("--dt", type=float, default=0.1)
    p.add_argument("--steps", type=int, default=20)

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "exponential-rate":
        rate = exponential_rate(args.state, args.growth_rate)
        emit(cmd, args, {"rate": rate}, "Computes dx/dt = r x.", "Exponential growth assumes no capacity constraint.")
    elif cmd == "logistic-rate":
        rate = logistic_rate(args.state, args.growth_rate, args.capacity)
        emit(cmd, args, {"rate": rate}, "Computes dx/dt = r x (1 - x/K).", "Logistic growth assumes a fixed carrying capacity.")
    elif cmd == "euler-step":
        next_state = euler_step(args.state, args.rate, args.dt)
        emit(cmd, args, {"next_state": next_state}, "Computes one explicit Euler update.")
    elif cmd == "simulate-exponential":
        rows = simulate_exponential(args.state, args.growth_rate, args.dt, args.steps)
        write_series("simulate_exponential", rows)
        emit(cmd, args, {"final_state": rows[-1]["state"], "records": len(rows)}, "Simulates exponential growth with explicit Euler.", "Check step-size sensitivity before interpretation.")
    elif cmd == "simulate-logistic":
        rows = simulate_logistic(args.state, args.growth_rate, args.capacity, args.dt, args.steps)
        write_series("simulate_logistic", rows)
        emit(cmd, args, {"final_state": rows[-1]["state"], "records": len(rows)}, "Simulates logistic growth with explicit Euler.", "Check capacity assumption and step-size sensitivity.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
