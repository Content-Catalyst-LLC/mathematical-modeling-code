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

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def exponential(n0: float, r: float, t: float) -> float:
    return n0 * math.exp(r * t)

def logistic(n0: float, r: float, k: float, t: float) -> float:
    if n0 <= 0 or k <= 0:
        raise ValueError("n0 and k must be positive.")
    return k / (1.0 + ((k - n0) / n0) * math.exp(-r * t))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("exponential")
    p.add_argument("--n0", type=float, default=100.0)
    p.add_argument("--r", type=float, default=0.08)
    p.add_argument("--t", type=float, default=40.0)

    p = sub.add_parser("logistic")
    p.add_argument("--n0", type=float, default=100.0)
    p.add_argument("--r", type=float, default=0.08)
    p.add_argument("--k", type=float, default=1000.0)
    p.add_argument("--t", type=float, default=40.0)

    p = sub.add_parser("per-capita")
    p.add_argument("--growth", type=float, default=8.0)
    p.add_argument("--population", type=float, default=100.0)

    p = sub.add_parser("equilibrium")
    p.add_argument("--r", type=float, default=0.08)
    p.add_argument("--k", type=float, default=1000.0)

    p = sub.add_parser("sensitivity-r")
    p.add_argument("--n0", type=float, default=100.0)
    p.add_argument("--r", type=float, default=0.08)
    p.add_argument("--k", type=float, default=1000.0)
    p.add_argument("--t", type=float, default=40.0)
    p.add_argument("--delta", type=float, default=0.01)

    p = sub.add_parser("capacity-warning")
    p.add_argument("--n", type=float, default=900.0)
    p.add_argument("--k", type=float, default=1000.0)
    p.add_argument("--margin", type=float, default=0.15)

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "exponential":
        value = exponential(args.n0, args.r, args.t)
        emit(cmd, args, {"population": value}, "Computes unconstrained continuous exponential population growth.", "Exponential growth is a baseline model and may overreach when constraints matter.")
    elif cmd == "logistic":
        value = logistic(args.n0, args.r, args.k, args.t)
        emit(cmd, args, {"population": value, "capacity_fraction": value / args.k}, "Computes capacity-limited logistic population growth.", "Carrying capacity is assumption-bearing and may change over time.")
    elif cmd == "per-capita":
        if args.population <= 0:
            raise ValueError("population must be positive")
        rate = args.growth / args.population
        emit(cmd, args, {"per_capita_rate": rate}, "Computes growth per unit population.", "Per-capita rates depend on population definition and time scale.")
    elif cmd == "equilibrium":
        equilibria = [0.0, args.k]
        stable_equilibrium = args.k if args.r > 0 else 0.0
        emit(cmd, args, {"equilibria": equilibria, "stable_equilibrium": stable_equilibrium}, "Returns logistic model equilibria under the basic continuous model.", "Equilibrium is a mathematical condition, not a complete interpretation.")
    elif cmd == "sensitivity-r":
        base = logistic(args.n0, args.r, args.k, args.t)
        perturbed = logistic(args.n0, args.r + args.delta, args.k, args.t)
        sensitivity = (perturbed - base) / args.delta
        emit(cmd, args, {"base_population": base, "perturbed_population": perturbed, "finite_difference_sensitivity": sensitivity}, "Approximates sensitivity of the logistic trajectory to the growth rate.", "Population projections can be highly sensitive to growth-rate assumptions.")
    elif cmd == "capacity-warning":
        if args.k <= 0:
            raise ValueError("k must be positive")
        fraction = args.n / args.k
        near = fraction >= 1.0 - args.margin
        emit(cmd, args, {"capacity_fraction": fraction, "near_capacity": near}, "Flags when a population is near modeled carrying capacity.", "Capacity warnings depend on the interpretation and uncertainty of K.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
