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

def lotka_step(x, y, alpha, beta, gamma, delta, dt):
    dx = alpha * x - beta * x * y
    dy = delta * x * y - gamma * y
    return max(0.0, x + dt * dx), max(0.0, y + dt * dy), dx, dy

def jacobian(alpha, beta, gamma, delta, x, y):
    return alpha - beta * y, -beta * x, delta * y, delta * x - gamma

def trace_det(j):
    a, b, c, d = j
    return a + d, a * d - b * c

def stability_status(trace, determinant):
    if determinant < 0:
        return "saddle"
    if determinant > 0 and abs(trace) < 1e-9:
        return "center_or_neutral_linearization"
    if determinant > 0 and trace < 0:
        return "locally_stable"
    if determinant > 0 and trace > 0:
        return "locally_unstable"
    return "degenerate_or_requires_review"

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("lotka-volterra-step")
    p.add_argument("--x", type=float, default=40.0)
    p.add_argument("--y", type=float, default=9.0)
    p.add_argument("--alpha", type=float, default=0.6)
    p.add_argument("--beta", type=float, default=0.02)
    p.add_argument("--gamma", type=float, default=0.5)
    p.add_argument("--delta", type=float, default=0.01)
    p.add_argument("--dt", type=float, default=0.02)

    p = sub.add_parser("coexistence")
    p.add_argument("--alpha", type=float, default=0.6)
    p.add_argument("--beta", type=float, default=0.02)
    p.add_argument("--gamma", type=float, default=0.5)
    p.add_argument("--delta", type=float, default=0.01)

    p = sub.add_parser("jacobian")
    p.add_argument("--x", type=float, default=50.0)
    p.add_argument("--y", type=float, default=30.0)
    p.add_argument("--alpha", type=float, default=0.6)
    p.add_argument("--beta", type=float, default=0.02)
    p.add_argument("--gamma", type=float, default=0.5)
    p.add_argument("--delta", type=float, default=0.01)

    p = sub.add_parser("simulate")
    p.add_argument("--x0", type=float, default=40.0)
    p.add_argument("--y0", type=float, default=9.0)
    p.add_argument("--alpha", type=float, default=0.6)
    p.add_argument("--beta", type=float, default=0.02)
    p.add_argument("--gamma", type=float, default=0.5)
    p.add_argument("--delta", type=float, default=0.01)
    p.add_argument("--dt", type=float, default=0.02)
    p.add_argument("--steps", type=int, default=4000)

    p = sub.add_parser("type-ii-response")
    p.add_argument("--x", type=float, default=50.0)
    p.add_argument("--a", type=float, default=0.04)
    p.add_argument("--h", type=float, default=0.08)

    p = sub.add_parser("harvesting-risk")
    p.add_argument("--hx", type=float, default=1.0)
    p.add_argument("--hy", type=float, default=0.05)

    p = sub.add_parser("interaction-warning")
    p.add_argument("--pattern", default="mass_action")

    return parser

def main() -> None:
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "lotka-volterra-step":
        x_next, y_next, dx, dy = lotka_step(args.x, args.y, args.alpha, args.beta, args.gamma, args.delta, args.dt)
        emit(cmd, args, {"dx": dx, "dy": dy, "x_next": x_next, "y_next": y_next}, "Computes one Euler step for the Lotka-Volterra model.", "One numerical step is not a validated ecological claim.")
    elif cmd == "coexistence":
        x_star = args.gamma / args.delta
        y_star = args.alpha / args.beta
        emit(cmd, args, {"x_star": x_star, "y_star": y_star}, "Computes the coexistence equilibrium for the classic model.", "Equilibrium is a mathematical condition, not a full ecological conclusion.")
    elif cmd == "jacobian":
        j = jacobian(args.alpha, args.beta, args.gamma, args.delta, args.x, args.y)
        tr, det = trace_det(j)
        emit(cmd, args, {"j11": j[0], "j12": j[1], "j21": j[2], "j22": j[3], "trace": tr, "determinant": det, "status": stability_status(tr, det)}, "Computes Jacobian entries and local stability summary.", "Local linearization depends on model structure and point of evaluation.")
    elif cmd == "simulate":
        x, y = args.x0, args.y0
        for _ in range(args.steps):
            x, y, _, _ = lotka_step(x, y, args.alpha, args.beta, args.gamma, args.delta, args.dt)
        emit(cmd, args, {"final_prey": x, "final_predator": y}, "Simulates a classic Lotka-Volterra scenario.", "Modeled cycles depend on ideal assumptions.")
    elif cmd == "type-ii-response":
        response = (args.a * args.x) / (1.0 + args.a * args.h * args.x)
        emit(cmd, args, {"functional_response": response}, "Computes Type II functional response per predator.", "Functional response choice can change stability and persistence conclusions.")
    elif cmd == "harvesting-risk":
        risk = "review" if args.hx > 0 or args.hy > 0 else "none"
        emit(cmd, args, {"harvesting_status": risk}, "Flags harvesting or removal terms for governance review.", "Management terms should be interpreted as policy assumptions.")
    elif cmd == "interaction-warning":
        notes = {
            "mass_action": "The product xy is an assumption, not universal evidence of encounter dynamics.",
            "functional_response": "The wrong functional response can change stability and persistence conclusions.",
            "cycle": "A modeled cycle is not automatically a confirmed ecological mechanism.",
            "stochastic": "A single stochastic path is not a distribution."
        }
        emit(cmd, args, {"note": notes.get(args.pattern, "Document the interaction assumption.")}, "Creates an interaction-assumption governance warning.", "Predator-prey conclusions should not exceed evidence, assumptions, and tested scope.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
