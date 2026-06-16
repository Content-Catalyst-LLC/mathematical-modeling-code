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

def logistic_solution(t: float, x0: float, r: float, k: float) -> float:
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

    p = sub.add_parser("initial-condition-effect")
    p.add_argument("--low", type=float, default=5.0)
    p.add_argument("--baseline", type=float, default=10.0)
    p.add_argument("--high", type=float, default=20.0)
    p.add_argument("--growth-rate", type=float, default=0.35)
    p.add_argument("--carrying-capacity", type=float, default=100.0)
    p.add_argument("--horizon", type=float, default=20.0)

    p = sub.add_parser("scope-check")
    p.add_argument("--value", type=float, default=0.35)
    p.add_argument("--lower", type=float, default=0.1)
    p.add_argument("--upper", type=float, default=0.6)

    p = sub.add_parser("boundary-warning")
    p.add_argument("--boundary-type", default="no_flux")

    p = sub.add_parser("horizon-warning")
    p.add_argument("--horizon", type=float, default=20.0)
    p.add_argument("--maximum-supported", type=float, default=20.0)

    p = sub.add_parser("condition-scope-warning")
    p.add_argument("--pattern", default="claim_boundary")

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "logistic-final":
        final = logistic_solution(args.horizon, args.initial_stock, args.growth_rate, args.carrying_capacity)
        emit(cmd, args, {"final_stock": final}, "Computes a logistic final state from an initial condition.", "Synthetic teaching example; do not treat as empirical forecast.")
    elif cmd == "initial-condition-effect":
        low = logistic_solution(args.horizon, args.low, args.growth_rate, args.carrying_capacity)
        baseline = logistic_solution(args.horizon, args.baseline, args.growth_rate, args.carrying_capacity)
        high = logistic_solution(args.horizon, args.high, args.growth_rate, args.carrying_capacity)
        emit(cmd, args, {"low_final": low, "baseline_final": baseline, "high_final": high, "low_effect": low - baseline, "high_effect": high - baseline}, "Compares final-state sensitivity to starting values.", "Initial-condition sensitivity changes interpretation.")
    elif cmd == "scope-check":
        in_scope = args.lower <= args.value <= args.upper
        emit(cmd, args, {"in_scope": in_scope}, "Checks whether a parameter is within documented scope.", "Using values outside tested ranges requires review.")
    elif cmd == "boundary-warning":
        notes = {
            "no_flux": "No-flux boundaries may overstate retention if the real system is open.",
            "absorbing": "Absorbing boundaries may understate feedback from surroundings.",
            "fixed": "Fixed boundary values can impose external behavior on the model.",
            "periodic": "Periodic boundaries may create artificial loops."
        }
        emit(cmd, args, {"boundary_type": args.boundary_type, "note": notes.get(args.boundary_type, "Document boundary assumptions and edge effects.")}, "Creates a boundary interpretation warning.", "Boundary assumptions can dominate model behavior.")
    elif cmd == "horizon-warning":
        within = args.horizon <= args.maximum_supported
        emit(cmd, args, {"within_supported_horizon": within}, "Checks whether a time horizon is within documented temporal scope.", "Short-horizon models should not be treated as long-term forecasts.")
    elif cmd == "condition-scope-warning":
        notes = {
            "initial_condition": "Initial conditions should include unit, source, uncertainty, and baseline notes.",
            "boundary_condition": "Boundary assumptions can dominate spatial model behavior.",
            "parameter_scope": "Using values outside tested ranges requires review.",
            "claim_boundary": "Model results should not be used beyond documented scope."
        }
        emit(cmd, args, {"pattern": args.pattern, "note": notes.get(args.pattern, "Document condition and scope limitations.")}, "Creates a condition and scope interpretation warning.", "Scope is the boundary of responsible use.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
