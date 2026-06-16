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

def logistic_step(stock: float, growth_rate: float, carrying_capacity: float, time_step: float) -> float:
    dx = growth_rate * stock * (1 - stock / carrying_capacity)
    return stock + time_step * dx

def simulate_final(growth_rate: float, carrying_capacity: float, initial_stock: float, time_step: float, horizon: float) -> tuple[float, float]:
    time = 0.0
    stock = initial_stock
    while time < horizon:
        stock = logistic_step(stock, growth_rate, carrying_capacity, time_step)
        time += time_step
    return time, stock

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("validate-parameter")
    p.add_argument("--name", default="growth_rate")
    p.add_argument("--value", type=float, default=0.35)
    p.add_argument("--minimum", type=float, default=0.0)

    p = sub.add_parser("logistic-step")
    p.add_argument("--stock", type=float, default=10.0)
    p.add_argument("--growth-rate", type=float, default=0.35)
    p.add_argument("--carrying-capacity", type=float, default=100.0)
    p.add_argument("--time-step", type=float, default=0.25)

    p = sub.add_parser("simulate-final")
    p.add_argument("--growth-rate", type=float, default=0.35)
    p.add_argument("--carrying-capacity", type=float, default=100.0)
    p.add_argument("--initial-stock", type=float, default=10.0)
    p.add_argument("--time-step", type=float, default=0.25)
    p.add_argument("--horizon", type=float, default=20.0)

    p = sub.add_parser("diagnostic-status")
    p.add_argument("--review-required", default="false")

    p = sub.add_parser("record-completeness")
    p.add_argument("--present", type=int, default=7)
    p.add_argument("--required", type=int, default=7)

    p = sub.add_parser("type-safety-warning")
    p.add_argument("--pattern", default="empirical_validity")

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "validate-parameter":
        valid = args.value > args.minimum
        emit(cmd, args, {"valid": valid, "message": "passed" if valid else f"{args.name} must be greater than {args.minimum}"}, "Checks a simple lower-bound parameter rule.", "Validation rules do not prove empirical correctness.")
    elif cmd == "logistic-step":
        next_stock = logistic_step(args.stock, args.growth_rate, args.carrying_capacity, args.time_step)
        emit(cmd, args, {"next_stock": next_stock}, "Computes one typed logistic transformation step.", "Pure transformations can still encode poor assumptions.")
    elif cmd == "simulate-final":
        final_time, final_stock = simulate_final(args.growth_rate, args.carrying_capacity, args.initial_stock, args.time_step, args.horizon)
        emit(cmd, args, {"final_time": final_time, "final_stock": final_stock}, "Simulates a typed model record to final time.", "Typed outputs still require diagnostics and interpretation limits.")
    elif cmd == "diagnostic-status":
        review = str(args.review_required).lower() in {"true", "1", "yes"}
        emit(cmd, args, {"status": "review_required" if review else "converged", "review_required": review}, "Creates a diagnostic status from a review flag.", "Diagnostics should remain attached to outputs.")
    elif cmd == "record-completeness":
        complete = args.present >= args.required
        emit(cmd, args, {"complete": complete, "missing": max(args.required - args.present, 0)}, "Checks whether a model record has required fields.", "Field presence does not prove field quality.")
    elif cmd == "type-safety-warning":
        notes = {
            "empirical_validity": "Type safety does not prove empirical validity.",
            "wrong_assumption": "A pure function can still encode the wrong mechanism.",
            "unit_confusion": "Unit notes or unit-specific types are needed to reduce interpretation errors.",
            "claim_boundary": "Typed outputs still require human judgment and claim boundaries."
        }
        emit(cmd, args, {"pattern": args.pattern, "note": notes.get(args.pattern, "Document typed workflow limitations and narrow the claim.")}, "Creates a type-safety interpretation warning.", "Type safety improves structure, not truth.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
