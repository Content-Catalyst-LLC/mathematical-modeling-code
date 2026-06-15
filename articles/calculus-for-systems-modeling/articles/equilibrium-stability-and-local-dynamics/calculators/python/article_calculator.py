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

def logistic_derivative(x: float, growth_rate: float, carrying_capacity: float) -> float:
    return growth_rate * (1.0 - 2.0 * x / carrying_capacity)

def bistable_rate(x: float, threshold: float) -> float:
    return x * (1.0 - x) * (x - threshold)

def numerical_derivative(model: str, state: float, threshold: float, h: float = 1e-5) -> float:
    if model == "bistable":
        f = lambda x: bistable_rate(x, threshold)
    else:
        raise ValueError(model)
    return (f(state + h) - f(state - h)) / (2.0 * h)

def classify_scalar_stability(derivative_value: float, tolerance: float = 1e-8) -> str:
    if derivative_value < -tolerance:
        return "locally_stable"
    if derivative_value > tolerance:
        return "locally_unstable"
    return "inconclusive_by_linearization"

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def write_series(name: str, rows: list[dict]) -> None:
    ensure_output_dir()
    (OUTPUT_DIR / f"{name}.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    with (OUTPUT_DIR / f"{name}.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("classify-derivative")
    p.add_argument("--derivative-value", type=float, default=-0.6)

    p = sub.add_parser("logistic-stability")
    p.add_argument("--equilibrium", type=float, default=100.0)
    p.add_argument("--growth-rate", type=float, default=0.6)
    p.add_argument("--carrying-capacity", type=float, default=100.0)

    p = sub.add_parser("bistable-stability")
    p.add_argument("--equilibrium", type=float, default=0.4)
    p.add_argument("--threshold", type=float, default=0.4)

    p = sub.add_parser("numerical-derivative")
    p.add_argument("--model", choices=["bistable"], default="bistable")
    p.add_argument("--state", type=float, default=0.4)
    p.add_argument("--threshold", type=float, default=0.4)

    p = sub.add_parser("equilibrium-table")
    p.add_argument("--growth-rate", type=float, default=0.6)
    p.add_argument("--carrying-capacity", type=float, default=100.0)
    p.add_argument("--threshold", type=float, default=0.4)

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "classify-derivative":
        stability = classify_scalar_stability(args.derivative_value)
        emit(cmd, args, {"stability": stability}, "Classifies scalar local stability from the derivative at equilibrium.", "Derivative tests are local and conditional on model form.")
    elif cmd == "logistic-stability":
        d = logistic_derivative(args.equilibrium, args.growth_rate, args.carrying_capacity)
        emit(cmd, args, {"derivative_value": d, "stability": classify_scalar_stability(d)}, "Evaluates local stability for a logistic equilibrium.", "Logistic stability assumes fixed carrying capacity and smooth density limitation.")
    elif cmd == "bistable-stability":
        d = numerical_derivative("bistable", args.equilibrium, args.threshold)
        emit(cmd, args, {"derivative_value": d, "stability": classify_scalar_stability(d)}, "Evaluates local stability for a bistable threshold equilibrium.", "Threshold stability depends on the assumed threshold and domain.")
    elif cmd == "numerical-derivative":
        d = numerical_derivative(args.model, args.state, args.threshold)
        emit(cmd, args, {"derivative_value": d}, "Computes a central-difference local derivative.", "Numerical derivatives depend on step size and smoothness.")
    elif cmd == "equilibrium-table":
        rows = []
        for eq in [0.0, args.carrying_capacity]:
            d = logistic_derivative(eq, args.growth_rate, args.carrying_capacity)
            rows.append({"scenario": "logistic_growth", "equilibrium": eq, "derivative_value": d, "stability": classify_scalar_stability(d)})
        for eq in [0.0, args.threshold, 1.0]:
            d = numerical_derivative("bistable", eq, args.threshold)
            rows.append({"scenario": "bistable_threshold", "equilibrium": eq, "derivative_value": d, "stability": classify_scalar_stability(d)})
        write_series("equilibrium_table", rows)
        emit(cmd, args, {"records": len(rows)}, "Builds a stability table for logistic and bistable examples.", "Stable, resilient, persistent, and desirable are not synonyms.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
