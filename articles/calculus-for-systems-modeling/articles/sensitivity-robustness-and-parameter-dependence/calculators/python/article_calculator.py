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

def logistic_final(x0: float, r: float, k: float, t: float) -> float:
    return k / (1 + ((k - x0) / x0) * math.exp(-r * t))

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("logistic-final")
    p.add_argument("--initial-stock", type=float, default=10.0)
    p.add_argument("--growth-rate", type=float, default=0.35)
    p.add_argument("--carrying-capacity", type=float, default=100.0)
    p.add_argument("--horizon", type=float, default=20.0)

    p = sub.add_parser("finite-difference")
    p.add_argument("--low-output", type=float, default=85.8)
    p.add_argument("--high-output", type=float, default=99.7)
    p.add_argument("--lower", type=float, default=0.2)
    p.add_argument("--upper", type=float, default=0.5)

    p = sub.add_parser("elasticity")
    p.add_argument("--sensitivity", type=float, default=46.3)
    p.add_argument("--parameter", type=float, default=0.35)
    p.add_argument("--output", type=float, default=99.2)

    p = sub.add_parser("robustness-classification")
    p.add_argument("--low-output", type=float, default=85.8)
    p.add_argument("--high-output", type=float, default=99.7)
    p.add_argument("--threshold", type=float, default=10.0)

    p = sub.add_parser("sweep-range")
    p.add_argument("--lower", type=float, default=0.2)
    p.add_argument("--upper", type=float, default=0.5)
    p.add_argument("--steps", type=int, default=7)

    p = sub.add_parser("sensitivity-warning")
    p.add_argument("--pattern", default="robustness_domain")

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "logistic-final":
        final = logistic_final(args.initial_stock, args.growth_rate, args.carrying_capacity, args.horizon)
        emit(cmd, args, {"final_output": final}, "Computes a logistic final output for a baseline parameter set.", "Synthetic teaching example; do not treat as empirical forecast.")
    elif cmd == "finite-difference":
        sensitivity = (args.high_output - args.low_output) / (args.upper - args.lower)
        emit(cmd, args, {"finite_difference_sensitivity": sensitivity}, "Estimates sensitivity from low and high parameter outputs.", "Finite differences depend on the tested range and may miss local nonlinear behavior.")
    elif cmd == "elasticity":
        elasticity = args.sensitivity * args.parameter / args.output if args.output != 0 else float("nan")
        emit(cmd, args, {"elasticity_estimate": elasticity}, "Computes relative output response to relative parameter change.", "Elasticity depends on the chosen baseline and output metric.")
    elif cmd == "robustness-classification":
        output_range = abs(args.high_output - args.low_output)
        status = "stable" if output_range < args.threshold else "sensitive"
        emit(cmd, args, {"output_range": output_range, "robustness_status": status}, "Classifies robustness from output variation over a tested range.", "Robustness depends on the tested parameter domain.")
    elif cmd == "sweep-range":
        if args.steps < 2:
            values = [args.lower]
        else:
            step = (args.upper - args.lower) / (args.steps - 1)
            values = [args.lower + i * step for i in range(args.steps)]
        emit(cmd, args, {"values": values, "count": len(values)}, "Builds an evenly spaced parameter sweep range.", "Sweep conclusions apply only over the tested range.")
    elif cmd == "sensitivity-warning":
        notes = {
            "local_only": "Local sensitivity may miss nonlinear or threshold behavior.",
            "baseline": "Sensitivity rankings depend on the chosen baseline.",
            "robustness_domain": "Robustness depends on the tested parameter domain.",
            "elasticity": "Elasticity depends on the output metric and reference parameter value.",
            "fragility": "Fragile conclusions require careful communication and review."
        }
        emit(cmd, args, {"pattern": args.pattern, "note": notes.get(args.pattern, "Document sensitivity limits and claim boundaries.")}, "Creates a sensitivity interpretation warning.", "Sensitivity analysis supports model review but does not prove model validity.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
