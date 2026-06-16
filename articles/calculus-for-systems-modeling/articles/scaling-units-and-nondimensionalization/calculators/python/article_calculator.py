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

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def rate_factor(from_unit: str, to_unit: str) -> float:
    per_year = {"day": 365.0, "month": 12.0, "year": 1.0, "hour": 24.0 * 365.0}
    if from_unit not in per_year or to_unit not in per_year:
        raise ValueError("supported units: hour, day, month, year")
    return per_year[from_unit] / per_year[to_unit]

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("scale-value")
    p.add_argument("--value", type=float, default=40.0)
    p.add_argument("--scale", type=float, default=100.0)

    p = sub.add_parser("unscale-value")
    p.add_argument("--dimensionless", type=float, default=0.4)
    p.add_argument("--scale", type=float, default=100.0)

    p = sub.add_parser("rate-conversion")
    p.add_argument("--rate", type=float, default=0.01)
    p.add_argument("--from-unit", default="day")
    p.add_argument("--to-unit", default="year")

    p = sub.add_parser("logistic-nondimensional")
    p.add_argument("--stock", type=float, default=40.0)
    p.add_argument("--capacity", type=float, default=100.0)
    p.add_argument("--time", type=float, default=20.0)
    p.add_argument("--growth-rate", type=float, default=0.35)

    p = sub.add_parser("conditioning-ratio")
    p.add_argument("--largest", type=float, default=1000000.0)
    p.add_argument("--smallest", type=float, default=0.001)

    p = sub.add_parser("scaling-warning")
    p.add_argument("--pattern", default="empirical_validity")

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "scale-value":
        emit(cmd, args, {"dimensionless_value": args.value / args.scale}, "Scales a dimensional value by a reference scale.", "Changing the reference scale changes dimensionless interpretation.")
    elif cmd == "unscale-value":
        emit(cmd, args, {"dimensional_value": args.dimensionless * args.scale}, "Recovers a dimensional value from a dimensionless value and reference scale.", "The recovered value depends on the documented reference scale.")
    elif cmd == "rate-conversion":
        converted = args.rate * rate_factor(args.from_unit, args.to_unit)
        emit(cmd, args, {"converted_rate": converted}, "Converts an inverse-time rate between common time units.", "Rate units must match the time variable.")
    elif cmd == "logistic-nondimensional":
        emit(cmd, args, {"scaled_stock": args.stock / args.capacity, "scaled_time": args.growth_rate * args.time}, "Computes nondimensional stock and time for a logistic model.", "Dimensionless form still depends on documented scale choices.")
    elif cmd == "conditioning-ratio":
        ratio = abs(args.largest / args.smallest) if args.smallest != 0 else float("inf")
        emit(cmd, args, {"conditioning_ratio": ratio, "large_scale_gap": ratio > 1e6}, "Computes a simple magnitude ratio for numerical scaling review.", "A large ratio can signal numerical conditioning concerns.")
    elif cmd == "scaling-warning":
        notes = {
            "unit_missing": "A numerical value without a unit may be ambiguous or misleading.",
            "scale_choice": "Changing the reference scale changes dimensionless interpretation.",
            "empirical_validity": "Scaling improves comparability but does not prove empirical validity.",
            "dimensionless_group": "Dimensionless groups require correct variable selection and interpretation.",
            "conversion": "Conversion rules should be explicit and reproducible."
        }
        emit(cmd, args, {"pattern": args.pattern, "note": notes.get(args.pattern, "Document scaling choices and interpretation boundaries.")}, "Creates a scaling interpretation warning.", "Nondimensionalization clarifies structure but does not replace evidence.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
