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

def predator_prey_rates(prey: float, predator: float, alpha: float, beta: float, delta: float, gamma: float) -> tuple[float, float]:
    return alpha*prey - beta*prey*predator, delta*prey*predator - gamma*predator

def coexistence_equilibrium(alpha: float, beta: float, delta: float, gamma: float) -> tuple[float, float]:
    return gamma / delta, alpha / beta

def euler_step(prey: float, predator: float, alpha: float, beta: float, delta: float, gamma: float, dt: float) -> dict:
    prey_rate, predator_rate = predator_prey_rates(prey, predator, alpha, beta, delta, gamma)
    return {
        "next_prey": max(0.0, prey + dt*prey_rate),
        "next_predator": max(0.0, predator + dt*predator_rate),
        "prey_rate": prey_rate,
        "predator_rate": predator_rate
    }

def simulate(prey: float, predator: float, alpha: float, beta: float, delta: float, gamma: float, dt: float, steps: int) -> list[dict]:
    rows = []
    for n in range(steps + 1):
        t = n*dt
        prey_rate, predator_rate = predator_prey_rates(prey, predator, alpha, beta, delta, gamma)
        rows.append({"step": n, "time": t, "prey": prey, "predator": predator, "prey_rate": prey_rate, "predator_rate": predator_rate})
        prey = max(0.0, prey + dt*prey_rate)
        predator = max(0.0, predator + dt*predator_rate)
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

def add_params(p):
    p.add_argument("--alpha", type=float, default=0.7)
    p.add_argument("--beta", type=float, default=0.05)
    p.add_argument("--delta", type=float, default=0.02)
    p.add_argument("--gamma", type=float, default=0.5)

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("predator-prey-rates")
    p.add_argument("--prey", type=float, default=40.0)
    p.add_argument("--predator", type=float, default=9.0)
    add_params(p)

    p = sub.add_parser("coexistence-equilibrium")
    add_params(p)

    p = sub.add_parser("euler-step")
    p.add_argument("--prey", type=float, default=40.0)
    p.add_argument("--predator", type=float, default=9.0)
    add_params(p)
    p.add_argument("--dt", type=float, default=0.01)

    p = sub.add_parser("simulate-predator-prey")
    p.add_argument("--prey", type=float, default=40.0)
    p.add_argument("--predator", type=float, default=9.0)
    add_params(p)
    p.add_argument("--dt", type=float, default=0.01)
    p.add_argument("--steps", type=int, default=100)

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "predator-prey-rates":
        prey_rate, predator_rate = predator_prey_rates(args.prey, args.predator, args.alpha, args.beta, args.delta, args.gamma)
        emit(cmd, args, {"prey_rate": prey_rate, "predator_rate": predator_rate}, "Computes coupled predator-prey derivative values.", "Assumes continuous well-mixed interaction.")
    elif cmd == "coexistence-equilibrium":
        prey_star, predator_star = coexistence_equilibrium(args.alpha, args.beta, args.delta, args.gamma)
        emit(cmd, args, {"coexistence_prey": prey_star, "coexistence_predator": predator_star}, "Computes the positive coexistence equilibrium for the illustrative system.", "Equilibrium is conditional on parameter values and model structure.")
    elif cmd == "euler-step":
        result = euler_step(args.prey, args.predator, args.alpha, args.beta, args.delta, args.gamma, args.dt)
        emit(cmd, args, result, "Computes one explicit Euler step for a coupled system.", "Euler error depends on step size.")
    elif cmd == "simulate-predator-prey":
        rows = simulate(args.prey, args.predator, args.alpha, args.beta, args.delta, args.gamma, args.dt, args.steps)
        write_series("simulate_predator_prey", rows)
        emit(cmd, args, {"records": len(rows), "final_prey": rows[-1]["prey"], "final_predator": rows[-1]["predator"]}, "Simulates an illustrative predator-prey coupled system.", "Check solver sensitivity and parameter uncertainty before interpretation.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
