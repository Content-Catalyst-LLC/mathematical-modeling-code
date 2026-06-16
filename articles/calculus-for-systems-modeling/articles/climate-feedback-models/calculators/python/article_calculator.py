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

def co2_forcing(concentration: float, baseline: float) -> float:
    return 5.35 * math.log(concentration / baseline)

def one_box(forcing: float, feedback: float, heat_capacity: float, time: float) -> float:
    equilibrium = forcing / feedback
    return equilibrium * (1.0 - math.exp(-(feedback / heat_capacity) * time))

def two_box(forcing: float, feedback: float, surface_capacity: float, deep_capacity: float, exchange: float, time: float, dt: float = 0.25):
    surface = 0.0
    deep = 0.0
    steps = int(time / dt)
    for _ in range(steps):
        d_surface = (forcing - feedback * surface - exchange * (surface - deep)) / surface_capacity
        d_deep = exchange * (surface - deep) / deep_capacity
        surface += dt * d_surface
        deep += dt * d_deep
    return surface, deep

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("co2-forcing")
    p.add_argument("--concentration", type=float, default=560.0)
    p.add_argument("--baseline", type=float, default=280.0)

    p = sub.add_parser("one-box")
    p.add_argument("--forcing", type=float, default=3.7)
    p.add_argument("--feedback", type=float, default=1.2)
    p.add_argument("--heat-capacity", type=float, default=8.0)
    p.add_argument("--time", type=float, default=80.0)

    p = sub.add_parser("ecs")
    p.add_argument("--forcing", type=float, default=3.7)
    p.add_argument("--feedback", type=float, default=1.2)

    p = sub.add_parser("feedback-sensitivity")
    p.add_argument("--forcing", type=float, default=3.7)
    p.add_argument("--feedback", type=float, default=1.2)

    p = sub.add_parser("two-box")
    p.add_argument("--forcing", type=float, default=3.7)
    p.add_argument("--feedback", type=float, default=1.2)
    p.add_argument("--surface-capacity", type=float, default=8.0)
    p.add_argument("--deep-capacity", type=float, default=100.0)
    p.add_argument("--exchange", type=float, default=0.7)
    p.add_argument("--time", type=float, default=80.0)

    p = sub.add_parser("carbon-feedback")
    p.add_argument("--forcing", type=float, default=3.7)
    p.add_argument("--temperature", type=float, default=3.0)
    p.add_argument("--beta-carbon", type=float, default=0.15)

    p = sub.add_parser("sign-warning")
    p.add_argument("--convention", default="restoring_positive")

    return parser

def main() -> None:
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "co2-forcing":
        value = co2_forcing(args.concentration, args.baseline)
        emit(cmd, args, {"forcing": value}, "Computes a simplified logarithmic CO2 radiative forcing approximation.", "This compact approximation does not replace detailed radiative-transfer modeling.")
    elif cmd == "one-box":
        value = one_box(args.forcing, args.feedback, args.heat_capacity, args.time)
        emit(cmd, args, {"temperature": value, "equilibrium_temperature": args.forcing / args.feedback}, "Computes one-box energy-balance temperature response.", "One-box models clarify structure but are not complete Earth-system models.")
    elif cmd == "ecs":
        value = args.forcing / args.feedback
        emit(cmd, args, {"equilibrium_response": value}, "Computes simplified equilibrium response under fixed forcing and restoring feedback.", "Equilibrium response should not be confused with near-term forecast.")
    elif cmd == "feedback-sensitivity":
        derivative = -args.forcing / (args.feedback ** 2)
        emit(cmd, args, {"dT_dlambda": derivative}, "Computes equilibrium sensitivity to feedback strength under restoring-positive convention.", "Feedback sign convention and uncertainty must be documented.")
    elif cmd == "two-box":
        surface, deep = two_box(args.forcing, args.feedback, args.surface_capacity, args.deep_capacity, args.exchange, args.time)
        emit(cmd, args, {"surface_temperature": surface, "deep_ocean_temperature": deep}, "Computes simplified two-box surface/deep-ocean heat uptake response.", "Ocean uptake controls transient response and committed warming.")
    elif cmd == "carbon-feedback":
        adjusted = args.forcing + args.beta_carbon * args.temperature
        emit(cmd, args, {"adjusted_forcing": adjusted}, "Computes simplified warming-dependent carbon-cycle feedback forcing.", "Carbon-cycle feedback is process-dependent and uncertain.")
    elif cmd == "sign-warning":
        notes = {
            "restoring_positive": "Using C dT/dt = F - lambda T, larger positive lambda means stronger damping.",
            "climate_feedback": "Some climate literature uses signs where negative feedback values are stabilizing and positive values are amplifying.",
        }
        emit(cmd, args, {"note": notes.get(args.convention, "Document feedback sign convention explicitly.")}, "Creates a sign-convention governance warning.", "Feedback signs must be stated before comparing parameters.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
