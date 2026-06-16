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
    p = sub.add_parser("equilibrium-temperature"); p.add_argument("--forcing", type=float, default=3.7); p.add_argument("--feedback", type=float, default=1.2)
    p = sub.add_parser("adjustment-time"); p.add_argument("--heat-capacity", type=float, default=10.0); p.add_argument("--feedback", type=float, default=1.2)
    p = sub.add_parser("absorbed-solar"); p.add_argument("--solar-constant", type=float, default=1361.0); p.add_argument("--albedo", type=float, default=0.30)
    p = sub.add_parser("one-layer-step"); p.add_argument("--temperature", type=float, default=0.0); p.add_argument("--forcing", type=float, default=3.7); p.add_argument("--feedback", type=float, default=1.2); p.add_argument("--heat-capacity", type=float, default=10.0); p.add_argument("--dt", type=float, default=1.0)
    p = sub.add_parser("surface-partition"); p.add_argument("--net-radiation", type=float, default=500.0); p.add_argument("--sensible", type=float, default=120.0); p.add_argument("--latent", type=float, default=300.0); p.add_argument("--ground", type=float, default=40.0)
    p = sub.add_parser("building-step"); p.add_argument("--temperature", type=float, default=20.0); p.add_argument("--heat-capacity", type=float, default=1000.0); p.add_argument("--q-heat", type=float, default=300.0); p.add_argument("--q-solar", type=float, default=150.0); p.add_argument("--q-internal", type=float, default=80.0); p.add_argument("--q-loss", type=float, default=420.0); p.add_argument("--dt", type=float, default=1.0)
    p = sub.add_parser("governance-warning"); p.add_argument("--context", default="boundary")
    return parser

def main() -> None:
    args = build_parser().parse_args()
    cmd = args.command
    if cmd == "equilibrium-temperature":
        emit(cmd, args, {"equilibrium_temperature": args.forcing / args.feedback}, "Computes simple equilibrium temperature response from forcing and feedback.", "Feedback terms can hide multiple physical processes.")
    elif cmd == "adjustment-time":
        emit(cmd, args, {"adjustment_time": args.heat_capacity / args.feedback}, "Computes adjustment time scale from heat capacity and feedback.", "Equilibrium should not be confused with immediate response.")
    elif cmd == "absorbed-solar":
        emit(cmd, args, {"absorbed_solar": args.solar_constant * (1 - args.albedo) / 4}, "Computes absorbed solar radiation under spherical averaging.", "Solar input requires albedo and geometry assumptions.")
    elif cmd == "one-layer-step":
        imbalance = args.forcing - args.feedback * args.temperature
        emit(cmd, args, {"imbalance": imbalance, "next_temperature": args.temperature + (imbalance / args.heat_capacity) * args.dt}, "Computes one one-layer energy balance update.", "Heat capacity must match the modeled reservoir.")
    elif cmd == "surface-partition":
        emit(cmd, args, {"storage_residual": args.net_radiation - args.sensible - args.latent - args.ground}, "Computes surface energy storage residual.", "Omitted surface energy terms change storage interpretation.")
    elif cmd == "building-step":
        imbalance = args.q_heat + args.q_solar + args.q_internal - args.q_loss
        emit(cmd, args, {"energy_imbalance": imbalance, "next_temperature": args.temperature + (imbalance / args.heat_capacity) * args.dt}, "Computes one building thermal balance update.", "Building thermal balance requires occupancy, weather, controls, and material assumptions.")
    elif cmd == "governance-warning":
        notes = {"boundary": "Energy balance conclusions are not meaningful without a defined boundary.", "storage": "Equilibrium should not be confused with immediate response.", "feedback": "Feedback terms can hide multiple physical processes.", "calibration": "A model can fit temperature while misrepresenting mechanism.", "flows": "Omitted flows can change the interpretation of imbalance."}
        emit(cmd, args, {"note": notes.get(args.context, "Document energy balance assumptions explicitly.")}, "Creates an energy balance governance warning.", "Energy balance conclusions should not exceed boundary definitions, data evidence, uncertainty, domain review, and tested scope.")

if __name__ == "__main__":
    main()
