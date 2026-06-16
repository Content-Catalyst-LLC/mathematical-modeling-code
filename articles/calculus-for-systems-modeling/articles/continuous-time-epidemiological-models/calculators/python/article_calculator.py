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

    p = sub.add_parser("r0")
    p.add_argument("--beta", type=float, default=0.32)
    p.add_argument("--gamma", type=float, default=0.10)

    p = sub.add_parser("rt")
    p.add_argument("--beta", type=float, default=0.32)
    p.add_argument("--gamma", type=float, default=0.10)
    p.add_argument("--susceptible", type=float, default=85000.0)
    p.add_argument("--population", type=float, default=100000.0)

    p = sub.add_parser("doubling-time")
    p.add_argument("--growth-rate", type=float, default=0.22)

    p = sub.add_parser("herd-threshold")
    p.add_argument("--r0", type=float, default=3.2)

    p = sub.add_parser("force-of-infection")
    p.add_argument("--beta", type=float, default=0.32)
    p.add_argument("--infectious", type=float, default=100.0)
    p.add_argument("--population", type=float, default=100000.0)

    p = sub.add_parser("incidence")
    p.add_argument("--beta", type=float, default=0.32)
    p.add_argument("--susceptible", type=float, default=99900.0)
    p.add_argument("--infectious", type=float, default=100.0)
    p.add_argument("--population", type=float, default=100000.0)

    p = sub.add_parser("sir-step")
    p.add_argument("--susceptible", type=float, default=99900.0)
    p.add_argument("--infectious", type=float, default=100.0)
    p.add_argument("--recovered", type=float, default=0.0)
    p.add_argument("--beta", type=float, default=0.32)
    p.add_argument("--gamma", type=float, default=0.10)
    p.add_argument("--population", type=float, default=100000.0)
    p.add_argument("--dt", type=float, default=1.0)

    p = sub.add_parser("governance-warning")
    p.add_argument("--context", default="reported_cases")

    return parser

def main() -> None:
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "r0":
        value = args.beta / args.gamma
        emit(cmd, args, {"r0": value}, "Computes the basic reproduction number for the simplest SIR convention.", "R0 depends on model structure, population, and context.")
    elif cmd == "rt":
        value = (args.beta / args.gamma) * (args.susceptible / args.population)
        emit(cmd, args, {"rt": value}, "Computes an effective reproduction number under a simple susceptible-share adjustment.", "Rt changes with susceptibility, behavior, intervention, and reporting context.")
    elif cmd == "doubling-time":
        value = math.inf if args.growth_rate <= 0 else math.log(2) / args.growth_rate
        emit(cmd, args, {"doubling_time": value}, "Computes exponential-growth doubling time.", "Doubling time is only valid under the assumed growth-rate window.")
    elif cmd == "herd-threshold":
        value = max(0.0, 1 - 1 / args.r0) if args.r0 > 0 else 0.0
        emit(cmd, args, {"herd_immunity_threshold": value}, "Computes the simple homogeneous-model herd-immunity threshold.", "Thresholds are model-dependent and should not be treated as public-health guarantees.")
    elif cmd == "force-of-infection":
        value = args.beta * args.infectious / args.population
        emit(cmd, args, {"force_of_infection": value}, "Computes force of infection in a homogeneous-mixing model.", "Transmission parameters can hide behavior, contact, biology, and environment.")
    elif cmd == "incidence":
        value = args.beta * args.susceptible * args.infectious / args.population
        emit(cmd, args, {"incidence": value}, "Computes the incidence flow from susceptible to infectious or exposed states.", "Reported cases should not be treated as true infections without observation assumptions.")
    elif cmd == "sir-step":
        new_inf = args.beta * args.susceptible * args.infectious / args.population
        recovery = args.gamma * args.infectious
        next_s = max(0.0, args.susceptible - new_inf * args.dt)
        next_i = max(0.0, args.infectious + (new_inf - recovery) * args.dt)
        next_r = min(args.population, args.recovered + recovery * args.dt)
        emit(cmd, args, {"new_infections": new_inf, "recoveries": recovery, "next_susceptible": next_s, "next_infectious": next_i, "next_recovered": next_r}, "Computes one SIR model step.", "This is an educational calculation, not medical advice or public-health guidance.")
    elif cmd == "governance-warning":
        notes = {
            "reported_cases": "Reported cases should not be treated as true infections without observation assumptions.",
            "transmission": "Transmission parameters can hide behavior, contact, biology, and environment.",
            "intervention": "Intervention effects should not be represented as unexplained reductions.",
            "threshold": "Thresholds are model-dependent summaries and should be presented with assumptions and context.",
            "guidance": "Educational scenarios are not medical advice, public-health guidance, or operational outbreak forecasts."
        }
        emit(cmd, args, {"note": notes.get(args.context, "Document epidemiological assumptions explicitly.")}, "Creates an epidemiological governance warning.", "Epidemiological conclusions should not exceed compartment definitions, data evidence, uncertainty, domain review, and tested scope.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
