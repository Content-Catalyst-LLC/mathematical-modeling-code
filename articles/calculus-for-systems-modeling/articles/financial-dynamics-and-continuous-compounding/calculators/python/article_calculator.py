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

def parse_cash_flows(raw: str) -> list[tuple[float, float]]:
    rows = []
    for item in raw.split(","):
        t, amount = item.split(":")
        rows.append((float(t), float(amount)))
    return rows

def parse_returns(raw: str) -> list[float]:
    return [float(x.strip()) for x in raw.split(",") if x.strip()]

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("continuous-future-value")
    p.add_argument("--v0", type=float, default=1000.0)
    p.add_argument("--r", type=float, default=0.05)
    p.add_argument("--t", type=float, default=30.0)

    p = sub.add_parser("continuous-present-value")
    p.add_argument("--fv", type=float, default=5000.0)
    p.add_argument("--r", type=float, default=0.05)
    p.add_argument("--t", type=float, default=30.0)

    p = sub.add_parser("discrete-compound-value")
    p.add_argument("--v0", type=float, default=1000.0)
    p.add_argument("--r", type=float, default=0.05)
    p.add_argument("--n", type=int, default=12)
    p.add_argument("--t", type=float, default=30.0)

    p = sub.add_parser("real-rate")
    p.add_argument("--nominal-rate", type=float, default=0.06)
    p.add_argument("--inflation-rate", type=float, default=0.025)

    p = sub.add_parser("npv")
    p.add_argument("--discount-rate", type=float, default=0.045)
    p.add_argument("--cash-flows", default="0:-1000,5:300,10:500,15:900,20:1200")

    p = sub.add_parser("debt-step")
    p.add_argument("--balance", type=float, default=2000.0)
    p.add_argument("--rate", type=float, default=0.07)
    p.add_argument("--payment", type=float, default=120.0)
    p.add_argument("--dt", type=float, default=1.0)

    p = sub.add_parser("geometric-return")
    p.add_argument("--returns", default="0.08,-0.12,0.15,0.04,-0.05,0.11")

    p = sub.add_parser("governance-warning")
    p.add_argument("--context", default="expected_return")

    return parser

def main() -> None:
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "continuous-future-value":
        value = args.v0 * math.exp(args.r * args.t)
        emit(cmd, args, {"future_value": value}, "Computes continuous-compounding future value.", "Long horizons amplify small rate differences.")
    elif cmd == "continuous-present-value":
        value = args.fv * math.exp(-args.r * args.t)
        emit(cmd, args, {"present_value": value}, "Computes continuous-discounting present value.", "Discount-rate choices can dominate long-horizon conclusions.")
    elif cmd == "discrete-compound-value":
        value = args.v0 * (1 + args.r / args.n) ** (args.n * args.t)
        emit(cmd, args, {"compound_value": value}, "Computes discrete-compounding future value.", "Compounding convention should match contract terms or model purpose.")
    elif cmd == "real-rate":
        value = (1 + args.nominal_rate) / (1 + args.inflation_rate) - 1
        emit(cmd, args, {"real_rate": value}, "Converts nominal return to real return using inflation adjustment.", "Cash flows and rates should use consistent real or nominal units.")
    elif cmd == "npv":
        flows = parse_cash_flows(args.cash_flows)
        value = sum(amount * math.exp(-args.discount_rate * time) for time, amount in flows)
        emit(cmd, args, {"net_present_value": value, "cash_flow_count": len(flows)}, "Computes continuous-discounted net present value.", "Cash-flow timing can dominate financial conclusions.")
    elif cmd == "debt-step":
        next_balance = max(0.0, args.balance + args.rate * args.balance * args.dt - args.payment * args.dt)
        emit(cmd, args, {"next_balance": next_balance, "interest_accrued": args.rate * args.balance * args.dt}, "Computes one debt balance update.", "Debt may grow if payment does not exceed interest accumulation.")
    elif cmd == "geometric-return":
        returns = parse_returns(args.returns)
        product = 1.0
        for r in returns:
            product *= (1 + r)
        value = product ** (1 / len(returns)) - 1
        emit(cmd, args, {"geometric_return": value, "period_count": len(returns)}, "Computes geometric mean return from period returns.", "Expected return does not guarantee realized compounded outcome.")
    elif cmd == "governance-warning":
        notes = {
            "expected_return": "Expected return does not guarantee realized compounded outcome.",
            "rate_convention": "Rate convention must be documented before comparing financial outcomes.",
            "cash_flow": "Cash-flow timing can dominate financial conclusions.",
            "discount_rate": "Discount-rate choices can dominate long-horizon conclusions.",
            "debt": "Debt may grow if payment does not exceed interest accumulation."
        }
        emit(cmd, args, {"note": notes.get(args.context, "Document financial assumptions explicitly.")}, "Creates a financial governance warning.", "Financial conclusions should not exceed rate conventions, cash-flow evidence, risk assumptions, uncertainty, and tested scope.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
