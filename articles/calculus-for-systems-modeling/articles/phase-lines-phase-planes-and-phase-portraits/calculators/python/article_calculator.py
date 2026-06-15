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

def predator_prey_rates(x: float, y: float, alpha: float, beta: float, delta: float, gamma: float) -> tuple[float, float]:
    return alpha*x - beta*x*y, delta*x*y - gamma*y

def phase_speed(dxdt: float, dydt: float) -> float:
    return math.sqrt(dxdt*dxdt + dydt*dydt)

def coexistence_equilibrium(alpha: float, beta: float, delta: float, gamma: float) -> tuple[float, float]:
    return gamma / delta, alpha / beta

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

    p = sub.add_parser("predator-prey-vector")
    p.add_argument("--x", type=float, default=40.0)
    p.add_argument("--y", type=float, default=9.0)
    add_params(p)

    p = sub.add_parser("phase-speed")
    p.add_argument("--dxdt", type=float, default=3.0)
    p.add_argument("--dydt", type=float, default=4.0)

    p = sub.add_parser("coexistence-equilibrium")
    add_params(p)

    p = sub.add_parser("grid-summary")
    p.add_argument("--x-max", type=int, default=60)
    p.add_argument("--y-max", type=int, default=30)
    p.add_argument("--x-step", type=int, default=5)
    p.add_argument("--y-step", type=int, default=3)

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "predator-prey-vector":
        dxdt, dydt = predator_prey_rates(args.x, args.y, args.alpha, args.beta, args.delta, args.gamma)
        emit(cmd, args, {"dxdt": dxdt, "dydt": dydt, "speed": phase_speed(dxdt, dydt)}, "Computes one vector-field point for a predator-prey phase plane.", "Vector-field values depend on parameter values and state ranges.")
    elif cmd == "phase-speed":
        emit(cmd, args, {"speed": phase_speed(args.dxdt, args.dydt)}, "Computes the magnitude of a phase-plane vector.", "Speed is a modeling and scaling-dependent quantity.")
    elif cmd == "coexistence-equilibrium":
        x_star, y_star = coexistence_equilibrium(args.alpha, args.beta, args.delta, args.gamma)
        emit(cmd, args, {"coexistence_x": x_star, "coexistence_y": y_star}, "Computes the positive coexistence equilibrium for the illustrative system.", "Equilibrium interpretation is conditional on model form and parameters.")
    elif cmd == "grid-summary":
        x_count = args.x_max // args.x_step + 1
        y_count = args.y_max // args.y_step + 1
        emit(cmd, args, {"x_points": x_count, "y_points": y_count, "total_grid_points": x_count*y_count}, "Summarizes a phase-portrait vector-field grid.", "Grid resolution affects the apparent density and smoothness of a phase portrait.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
