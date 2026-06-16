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

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("regeneration")
    p.add_argument("--stock", type=float, default=80.0)
    p.add_argument("--growth-rate", type=float, default=0.08)
    p.add_argument("--carrying-capacity", type=float, default=100.0)

    p = sub.add_parser("extraction")
    p.add_argument("--efficiency", type=float, default=0.003)
    p.add_argument("--effort", type=float, default=12.0)
    p.add_argument("--stock", type=float, default=80.0)

    p = sub.add_parser("stock-step")
    p.add_argument("--stock", type=float, default=80.0)
    p.add_argument("--growth-rate", type=float, default=0.08)
    p.add_argument("--carrying-capacity", type=float, default=100.0)
    p.add_argument("--harvest", type=float, default=2.88)
    p.add_argument("--stress", type=float, default=0.25)
    p.add_argument("--dt", type=float, default=0.25)

    p = sub.add_parser("adaptive-effort-step")
    p.add_argument("--effort", type=float, default=12.0)
    p.add_argument("--scarcity", type=float, default=0.2)
    p.add_argument("--governance-strength", type=float, default=0.6)
    p.add_argument("--adjustment-rate", type=float, default=0.2)
    p.add_argument("--dt", type=float, default=0.25)

    p = sub.add_parser("distributional-burden")
    p.add_argument("--exposure", type=float, default=0.6)
    p.add_argument("--vulnerability", type=float, default=1.4)
    p.add_argument("--adaptation", type=float, default=0.2)

    p = sub.add_parser("threshold-warning")
    p.add_argument("--stock", type=float, default=25.0)
    p.add_argument("--threshold", type=float, default=30.0)

    p = sub.add_parser("governance-warning")
    p.add_argument("--context", default="equity")

    return parser

def main() -> None:
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "regeneration":
        value = args.growth_rate * args.stock * (1 - args.stock / args.carrying_capacity)
        emit(cmd, args, {"regeneration": value}, "Computes logistic regeneration at the current stock.", "Regeneration may vary with habitat, climate, age structure, and system state.")
    elif cmd == "extraction":
        value = args.efficiency * args.effort * args.stock
        emit(cmd, args, {"extraction": value}, "Computes effort-based extraction pressure.", "Extraction assumptions should include technology, livelihoods, markets, and constraints.")
    elif cmd == "stock-step":
        regen = args.growth_rate * args.stock * (1 - args.stock / args.carrying_capacity)
        next_stock = max(0.0, args.stock + (regen - args.harvest - args.stress) * args.dt)
        emit(cmd, args, {"regeneration": regen, "next_stock": next_stock}, "Computes one natural-stock update.", "Stock dynamics require boundary, stress, extraction, and regeneration assumptions.")
    elif cmd == "adaptive-effort-step":
        next_effort = max(0.0, args.effort - args.adjustment_rate * args.governance_strength * args.scarcity * args.dt)
        emit(cmd, args, {"next_effort": next_effort}, "Computes one adaptive effort update.", "Human response may be slow, unequal, or constrained.")
    elif cmd == "distributional-burden":
        value = max(0.0, args.exposure * args.vulnerability - args.adaptation)
        emit(cmd, args, {"distributional_burden": value}, "Computes a simple distributional burden measure.", "Aggregate outcomes can hide unequal burden and environmental injustice.")
    elif cmd == "threshold-warning":
        status = "below_threshold_review_required" if args.stock < args.threshold else "above_threshold_monitoring_required"
        emit(cmd, args, {"threshold_status": status}, "Creates a threshold-status warning.", "Thresholds are uncertain and should be stress-tested.")
    elif cmd == "governance-warning":
        notes = {
            "boundary": "Coupled-system conclusions are not meaningful without a defined boundary and external-flow record.",
            "human": "Human assumptions should include constraints, institutions, rights, and distribution where relevant.",
            "natural": "Ecological assumptions should include uncertainty, thresholds, and omitted mechanisms.",
            "coupling": "Coupling terms should represent mechanisms, not just arrows.",
            "governance": "Governance should not be treated as a fixed or neutral constant without justification.",
            "equity": "Aggregate efficiency can hide unequal burden, displacement, and environmental injustice."
        }
        emit(cmd, args, {"note": notes.get(args.context, "Document coupled-system assumptions explicitly.")}, "Creates a coupled-systems governance warning.", "Coupled-system conclusions should not exceed boundary definitions, data evidence, mechanism plausibility, uncertainty, equity review, and tested scope.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
