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

def logistic_regeneration(stock, r, k):
    return max(0.0, r * stock * (1 - stock / k))

def msy(r, k):
    return r * k / 4.0

def simulate_renewable(stock0, harvest, r, k, dt, steps, loss_rate=0.0):
    stock = stock0
    cumulative = 0.0
    for _ in range(steps):
        extraction = min(stock, harvest * dt)
        growth = logistic_regeneration(stock, r, k) * dt
        loss = max(0.0, loss_rate * stock * dt)
        stock = max(0.0, stock + growth - extraction - loss)
        cumulative += extraction
    return stock, cumulative

def simulate_nonrenewable(stock0, extraction_rate, dt, steps):
    stock = stock0
    cumulative = 0.0
    for _ in range(steps):
        extraction = min(stock, extraction_rate * dt)
        stock = max(0.0, stock - extraction)
        cumulative += extraction
    return stock, cumulative

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("logistic-regeneration")
    p.add_argument("--stock", type=float, default=500.0)
    p.add_argument("--r", type=float, default=0.18)
    p.add_argument("--k", type=float, default=1000.0)

    p = sub.add_parser("msy")
    p.add_argument("--r", type=float, default=0.18)
    p.add_argument("--k", type=float, default=1000.0)
    p.add_argument("--precautionary-fraction", type=float, default=0.7)

    p = sub.add_parser("depletion-condition")
    p.add_argument("--regeneration", type=float, default=35.0)
    p.add_argument("--harvest", type=float, default=45.0)
    p.add_argument("--loss", type=float, default=5.0)

    p = sub.add_parser("simulate-renewable")
    p.add_argument("--stock0", type=float, default=600.0)
    p.add_argument("--harvest", type=float, default=35.0)
    p.add_argument("--r", type=float, default=0.18)
    p.add_argument("--k", type=float, default=1000.0)
    p.add_argument("--dt", type=float, default=0.1)
    p.add_argument("--steps", type=int, default=800)
    p.add_argument("--loss-rate", type=float, default=0.0)

    p = sub.add_parser("simulate-nonrenewable")
    p.add_argument("--stock0", type=float, default=600.0)
    p.add_argument("--extraction-rate", type=float, default=30.0)
    p.add_argument("--dt", type=float, default=0.1)
    p.add_argument("--steps", type=int, default=800)

    p = sub.add_parser("threshold-risk")
    p.add_argument("--stock", type=float, default=150.0)
    p.add_argument("--threshold", type=float, default=180.0)

    p = sub.add_parser("efficiency-rebound")
    p.add_argument("--demand", type=float, default=60.0)
    p.add_argument("--efficiency-gain", type=float, default=0.15)
    p.add_argument("--rebound-factor", type=float, default=0.6)

    p = sub.add_parser("governance-warning")
    p.add_argument("--context", default="msy")

    return parser

def main() -> None:
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "logistic-regeneration":
        value = logistic_regeneration(args.stock, args.r, args.k)
        emit(cmd, args, {"regeneration": value}, "Computes logistic resource regeneration.", "Logistic regeneration is a simplifying assumption and should be validated for the resource.")
    elif cmd == "msy":
        value = msy(args.r, args.k)
        emit(cmd, args, {"maximum_sustainable_yield": value, "precautionary_yield": value * args.precautionary_fraction}, "Computes idealized maximum sustainable yield and a precautionary yield.", "MSY is not a safe target under uncertainty by default.")
    elif cmd == "depletion-condition":
        net = args.regeneration - args.harvest - args.loss
        emit(cmd, args, {"net_change_rate": net, "depleting": net < 0}, "Checks whether extraction and losses exceed regeneration.", "A positive or negative rate must be interpreted with uncertainty and governance context.")
    elif cmd == "simulate-renewable":
        stock, cumulative = simulate_renewable(args.stock0, args.harvest, args.r, args.k, args.dt, args.steps, args.loss_rate)
        emit(cmd, args, {"final_stock": stock, "cumulative_extraction": cumulative}, "Simulates a renewable resource with logistic regeneration.", "Simulation output depends on stock definition, regeneration assumptions, and harvest governance.")
    elif cmd == "simulate-nonrenewable":
        stock, cumulative = simulate_nonrenewable(args.stock0, args.extraction_rate, args.dt, args.steps)
        emit(cmd, args, {"final_stock": stock, "cumulative_extraction": cumulative}, "Simulates nonrenewable resource drawdown.", "Nonrenewable drawdown should be modeled separately from renewable recovery.")
    elif cmd == "threshold-risk":
        status = "below_threshold" if args.stock < args.threshold else "above_threshold"
        emit(cmd, args, {"threshold_status": status, "stock_gap": args.stock - args.threshold}, "Flags whether stock is below a critical recovery threshold.", "Threshold values require evidence and precaution.")
    elif cmd == "efficiency-rebound":
        technical_reduction = args.demand * args.efficiency_gain
        rebound = technical_reduction * args.rebound_factor
        adjusted = max(0.0, args.demand - technical_reduction + rebound)
        emit(cmd, args, {"technical_reduction": technical_reduction, "rebound": rebound, "adjusted_extraction": adjusted}, "Estimates extraction after efficiency and rebound.", "Efficiency can create rebound if total demand rises.")
    elif cmd == "governance-warning":
        notes = {
            "msy": "MSY is not a safe target under uncertainty by default.",
            "renewable": "Renewable does not mean unlimited.",
            "extraction": "Extraction should not be treated as controllable without governance assumptions.",
            "threshold": "Threshold values require evidence and precaution.",
            "common_pool": "Common-pool resources require access, monitoring, enforcement, and equity records."
        }
        emit(cmd, args, {"note": notes.get(args.context, "Document resource governance assumptions explicitly.")}, "Creates a resource-governance warning.", "Resource conclusions should not exceed stock definitions, evidence, assumptions, governance feasibility, uncertainty, and tested scope.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
