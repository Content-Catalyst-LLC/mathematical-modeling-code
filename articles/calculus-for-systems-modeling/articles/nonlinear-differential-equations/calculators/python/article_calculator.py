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

def logistic_rate(x: float, growth_rate: float, carrying_capacity: float) -> float:
    return growth_rate*x*(1.0 - x/carrying_capacity)

def bistable_rate(x: float, threshold: float) -> float:
    return x*(1.0-x)*(x-threshold)

def euler_step(model: str, state: float, dt: float, growth_rate: float, carrying_capacity: float, threshold: float) -> dict:
    if model == "logistic":
        rate = logistic_rate(state, growth_rate, carrying_capacity)
    elif model == "bistable":
        rate = bistable_rate(state, threshold)
    else:
        raise ValueError(model)
    return {"rate": rate, "next_state": state + dt*rate}

def simulate(model: str, state: float, dt: float, steps: int, growth_rate: float, carrying_capacity: float, threshold: float) -> list[dict]:
    rows = []
    x = state
    for n in range(steps + 1):
        if model == "logistic":
            rate = logistic_rate(x, growth_rate, carrying_capacity)
        elif model == "bistable":
            rate = bistable_rate(x, threshold)
        else:
            raise ValueError(model)
        rows.append({"step": n, "time": n*dt, "state": x, "rate": rate})
        x = x + dt*rate
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

    p = sub.add_parser("logistic-rate")
    p.add_argument("--state", type=float, default=10.0)
    p.add_argument("--growth-rate", type=float, default=0.6)
    p.add_argument("--carrying-capacity", type=float, default=100.0)

    p = sub.add_parser("logistic-equilibria")
    p.add_argument("--carrying-capacity", type=float, default=100.0)

    p = sub.add_parser("bistable-rate")
    p.add_argument("--state", type=float, default=0.35)
    p.add_argument("--threshold", type=float, default=0.4)

    p = sub.add_parser("bistable-equilibria")
    p.add_argument("--threshold", type=float, default=0.4)

    p = sub.add_parser("euler-step")
    p.add_argument("--model", choices=["logistic", "bistable"], default="logistic")
    p.add_argument("--state", type=float, default=10.0)
    p.add_argument("--dt", type=float, default=0.05)
    p.add_argument("--growth-rate", type=float, default=0.6)
    p.add_argument("--carrying-capacity", type=float, default=100.0)
    p.add_argument("--threshold", type=float, default=0.4)

    p = sub.add_parser("simulate")
    p.add_argument("--model", choices=["logistic", "bistable"], default="logistic")
    p.add_argument("--state", type=float, default=10.0)
    p.add_argument("--dt", type=float, default=0.05)
    p.add_argument("--steps", type=int, default=100)
    p.add_argument("--growth-rate", type=float, default=0.6)
    p.add_argument("--carrying-capacity", type=float, default=100.0)
    p.add_argument("--threshold", type=float, default=0.4)

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "logistic-rate":
        rate = logistic_rate(args.state, args.growth_rate, args.carrying_capacity)
        emit(cmd, args, {"rate": rate}, "Computes the logistic nonlinear rate.", "Assumes fixed carrying capacity and smooth density limitation.")
    elif cmd == "logistic-equilibria":
        emit(cmd, args, {"equilibria": [0.0, args.carrying_capacity]}, "Returns logistic equilibrium points.", "Equilibria are conditional on model form and domain.")
    elif cmd == "bistable-rate":
        rate = bistable_rate(args.state, args.threshold)
        emit(cmd, args, {"rate": rate}, "Computes a bistable threshold nonlinear rate.", "Threshold requires evidence or explicit scenario labeling.")
    elif cmd == "bistable-equilibria":
        emit(cmd, args, {"equilibria": [0.0, args.threshold, 1.0]}, "Returns bistable threshold equilibrium points.", "Stability and interpretation require domain review.")
    elif cmd == "euler-step":
        result = euler_step(args.model, args.state, args.dt, args.growth_rate, args.carrying_capacity, args.threshold)
        emit(cmd, args, result, "Computes one explicit Euler update for a nonlinear scalar equation.", "Euler error depends on step size.")
    elif cmd == "simulate":
        rows = simulate(args.model, args.state, args.dt, args.steps, args.growth_rate, args.carrying_capacity, args.threshold)
        write_series(f"simulate_{args.model}", rows)
        emit(cmd, args, {"records": len(rows), "final_state": rows[-1]["state"], "final_rate": rows[-1]["rate"]}, "Simulates a nonlinear scalar differential equation.", "Check solver sensitivity and parameter uncertainty before interpretation.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
