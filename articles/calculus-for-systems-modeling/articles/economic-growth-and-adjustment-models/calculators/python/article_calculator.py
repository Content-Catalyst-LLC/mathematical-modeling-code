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

def ensure() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def write(name: str, payload: CalculatorResult) -> None:
    ensure()
    (OUTPUT_DIR / f"{name}.json").write_text(json.dumps(asdict(payload), indent=2, sort_keys=True), encoding="utf-8")
    flat = {"calculator": payload.calculator, "interpretation": payload.interpretation, "warning": payload.warning}
    flat.update({f"input_{k}": v for k, v in payload.inputs.items()})
    flat.update({f"result_{k}": v for k, v in payload.result.items() if not isinstance(v, list)})
    with (OUTPUT_DIR / f"{name}.csv").open("w", newline="", encoding="utf-8") as h:
        writer = csv.DictWriter(h, fieldnames=list(flat.keys()))
        writer.writeheader()
        writer.writerow(flat)

def emit(cmd: str, args, result: dict, interpretation: str, warning: str = "") -> None:
    payload = CalculatorResult(cmd, vars(args), result, interpretation, warning)
    write(cmd.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("exponential-growth")
    p.add_argument("--y0", type=float, default=100.0)
    p.add_argument("--g", type=float, default=0.025)
    p.add_argument("--years", type=float, default=40.0)

    p = sub.add_parser("doubling-time")
    p.add_argument("--g", type=float, default=0.025)

    p = sub.add_parser("logistic-growth")
    p.add_argument("--y0", type=float, default=100.0)
    p.add_argument("--r", type=float, default=0.06)
    p.add_argument("--k", type=float, default=240.0)
    p.add_argument("--years", type=int, default=40)

    p = sub.add_parser("capital-step")
    p.add_argument("--capital", type=float, default=300.0)
    p.add_argument("--output", type=float, default=100.0)
    p.add_argument("--savings-rate", type=float, default=0.22)
    p.add_argument("--depreciation", type=float, default=0.05)
    p.add_argument("--dt", type=float, default=1.0)

    p = sub.add_parser("cobb-douglas")
    p.add_argument("--a", type=float, default=1.2)
    p.add_argument("--k", type=float, default=450.0)
    p.add_argument("--l", type=float, default=180.0)
    p.add_argument("--alpha", type=float, default=0.35)

    p = sub.add_parser("growth-accounting")
    p.add_argument("--a-growth", type=float, default=0.01)
    p.add_argument("--k-growth", type=float, default=0.03)
    p.add_argument("--l-growth", type=float, default=0.02)
    p.add_argument("--alpha", type=float, default=0.35)

    p = sub.add_parser("adjustment-step")
    p.add_argument("--x", type=float, default=100.0)
    p.add_argument("--target", type=float, default=160.0)
    p.add_argument("--lambda-rate", type=float, default=0.35)
    p.add_argument("--dt", type=float, default=1.0)

    p = sub.add_parser("governance-warning")
    p.add_argument("--context", default="output_welfare")

    return parser

def main() -> None:
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "exponential-growth":
        final = args.y0 * math.exp(args.g * args.years)
        emit(cmd, args, {"final_output": final}, "Computes continuous exponential growth.", "Growth-rate assumptions compound strongly over time.")
    elif cmd == "doubling-time":
        dt = math.inf if args.g <= 0 else math.log(2) / args.g
        emit(cmd, args, {"doubling_time": dt}, "Computes continuous-growth doubling time.", "Doubling time assumes constant proportional growth.")
    elif cmd == "logistic-growth":
        y = args.y0
        for _ in range(args.years):
            y = max(0.0, y + args.r * y * (1 - y / args.k))
        emit(cmd, args, {"final_output": y}, "Computes constrained logistic growth.", "Constrained growth requires a defined mechanism and boundary.")
    elif cmd == "capital-step":
        investment = args.savings_rate * args.output
        next_capital = max(0.0, args.capital + (investment - args.depreciation * args.capital) * args.dt)
        emit(cmd, args, {"investment": investment, "next_capital": next_capital}, "Computes one capital accumulation step.", "Savings does not automatically become productive investment.")
    elif cmd == "cobb-douglas":
        output = args.a * (args.k ** args.alpha) * (args.l ** (1 - args.alpha))
        emit(cmd, args, {"output": output}, "Computes Cobb-Douglas output.", "Production functions simplify complex institutions, energy, skills, and organization.")
    elif cmd == "growth-accounting":
        growth = args.a_growth + args.alpha * args.k_growth + (1 - args.alpha) * args.l_growth
        emit(cmd, args, {"output_growth": growth}, "Computes Cobb-Douglas-style growth accounting.", "Productivity should not be used as an unexplained residual without interpretation.")
    elif cmd == "adjustment-step":
        next_x = args.x + args.lambda_rate * (args.target - args.x) * args.dt
        emit(cmd, args, {"next_value": next_x}, "Computes one adjustment step toward a target.", "Instant adjustment assumptions can hide overshoot and persistence.")
    elif cmd == "governance-warning":
        notes = {
            "output_welfare": "Output growth should not be treated as complete social progress.",
            "growth_rate": "Growth-rate assumptions compound strongly over time.",
            "productivity": "Productivity should not be used as a residual without interpretation.",
            "constraint": "Unconstrained growth assumptions should be compared with constrained scenarios.",
            "distribution": "Aggregate growth can hide distributional impacts."
        }
        emit(cmd, args, {"note": notes.get(args.context, "Document economic growth assumptions explicitly.")}, "Creates an economic-growth governance warning.", "Economic conclusions should not exceed output definitions, data evidence, structural assumptions, uncertainty, distributional interpretation, and tested scope.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
