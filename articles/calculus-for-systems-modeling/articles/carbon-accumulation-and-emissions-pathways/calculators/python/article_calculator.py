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

def linear_decline(e0, years):
    return [max(0.0, e0 * (1 - y / years)) for y in range(years + 1)]

def exponential_decline(e0, rate, years):
    return [e0 * math.exp(-rate * y) for y in range(years + 1)]

def overshoot_pathway(e0, decline_years, negative_years, removal_rate):
    return linear_decline(e0, decline_years) + [-removal_rate for _ in range(negative_years)]

def impulse_burden(pathway, persistent=0.2):
    coefficients = [(0.3, 4.0), (0.25, 35.0), (0.25, 200.0)]
    burden = 0.0
    horizon = len(pathway)
    for emission_year, emission in enumerate(pathway):
        age = horizon - 1 - emission_year
        response = persistent + sum(weight * math.exp(-age / tau) for weight, tau in coefficients)
        burden += emission * response
    return burden

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("cumulative-linear")
    p.add_argument("--e0", type=float, default=40.0)
    p.add_argument("--years", type=int, default=30)

    p = sub.add_parser("cumulative-exponential")
    p.add_argument("--e0", type=float, default=40.0)
    p.add_argument("--rate", type=float, default=0.08)
    p.add_argument("--years", type=int, default=30)

    p = sub.add_parser("atmospheric-burden")
    p.add_argument("--cumulative", type=float, default=600.0)
    p.add_argument("--airborne-fraction", type=float, default=0.45)

    p = sub.add_parser("budget-check")
    p.add_argument("--cumulative", type=float, default=600.0)
    p.add_argument("--budget", type=float, default=500.0)

    p = sub.add_parser("overshoot")
    p.add_argument("--e0", type=float, default=40.0)
    p.add_argument("--decline-years", type=int, default=30)
    p.add_argument("--negative-years", type=int, default=20)
    p.add_argument("--removal-rate", type=float, default=5.0)

    p = sub.add_parser("impulse-burden")
    p.add_argument("--e0", type=float, default=40.0)
    p.add_argument("--years", type=int, default=30)
    p.add_argument("--pathway", choices=["linear", "exponential", "constant"], default="linear")
    p.add_argument("--rate", type=float, default=0.08)

    p = sub.add_parser("removal-warning")
    p.add_argument("--gross", type=float, default=10.0)
    p.add_argument("--removal", type=float, default=10.0)

    p = sub.add_parser("accounting-warning")
    p.add_argument("--boundary", default="global_co2")

    return parser

def main() -> None:
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "cumulative-linear":
        pathway = linear_decline(args.e0, args.years)
        emit(cmd, args, {"cumulative_emissions": sum(pathway), "final_emissions": pathway[-1]}, "Computes cumulative emissions for a linear decline pathway.", "Linear decline still accumulates emissions until net zero.")
    elif cmd == "cumulative-exponential":
        pathway = exponential_decline(args.e0, args.rate, args.years)
        emit(cmd, args, {"cumulative_emissions": sum(pathway), "final_emissions": pathway[-1]}, "Computes cumulative emissions for an exponential decline pathway.", "Pathway assumptions should not be presented as predictions.")
    elif cmd == "atmospheric-burden":
        burden = args.cumulative * args.airborne_fraction
        emit(cmd, args, {"atmospheric_burden": burden}, "Computes simplified atmospheric burden using fixed airborne fraction.", "Airborne fraction is not constant across all time scales and scenarios.")
    elif cmd == "budget-check":
        overshoot = max(0.0, args.cumulative - args.budget)
        emit(cmd, args, {"exceeds_budget": args.cumulative > args.budget, "overshoot_amount": overshoot}, "Checks cumulative emissions against an illustrative carbon budget.", "Carbon budgets are conditional estimates, not exact guarantees.")
    elif cmd == "overshoot":
        pathway = overshoot_pathway(args.e0, args.decline_years, args.negative_years, args.removal_rate)
        emit(cmd, args, {"cumulative_emissions": sum(pathway), "minimum_emissions": min(pathway)}, "Computes cumulative emissions for an overshoot pathway with negative emissions.", "Negative emissions require feasibility, permanence, scale, and governance review.")
    elif cmd == "impulse-burden":
        if args.pathway == "linear":
            pathway = linear_decline(args.e0, args.years)
        elif args.pathway == "exponential":
            pathway = exponential_decline(args.e0, args.rate, args.years)
        else:
            pathway = [args.e0 for _ in range(args.years + 1)]
        emit(cmd, args, {"impulse_response_burden": impulse_burden(pathway), "cumulative_emissions": sum(pathway)}, "Computes an illustrative impulse-response atmospheric burden.", "Impulse response assumptions shape long-term burden.")
    elif cmd == "removal-warning":
        net = args.gross - args.removal
        emit(cmd, args, {"net_emissions": net, "net_zero_or_below": net <= 0}, "Separates gross emissions and removals.", "Net-zero and overshoot claims require removal governance.")
    elif cmd == "accounting-warning":
        notes = {
            "global_co2": "Global CO2 accounting should state emissions sources, units, and time horizon.",
            "net_emissions": "Net emissions should separate gross emissions and removals.",
            "corporate": "Corporate pathway accounting should document scope, boundaries, offsets, removals, and permanence.",
        }
        emit(cmd, args, {"note": notes.get(args.boundary, "Document accounting boundary explicitly.")}, "Creates an accounting-boundary governance warning.", "Carbon pathway conclusions should not exceed accounting boundaries, evidence, assumptions, uncertainty, and tested scope.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
