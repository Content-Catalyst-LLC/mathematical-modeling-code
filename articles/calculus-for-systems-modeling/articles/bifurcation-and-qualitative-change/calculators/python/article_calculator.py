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

def write_series(name: str, rows: list[dict]) -> None:
    ensure_output_dir()
    (OUTPUT_DIR / f"{name}.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    with (OUTPUT_DIR / f"{name}.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

def saddle_node_equilibria(mu: float) -> list[float]:
    if mu < 0:
        return []
    if abs(mu) < 1e-12:
        return [0.0]
    r = math.sqrt(mu)
    return [-r, r]

def transcritical_equilibria(mu: float) -> list[float]:
    return [0.0, mu]

def pitchfork_equilibria(mu: float) -> list[float]:
    if mu < 0:
        return [0.0]
    if abs(mu) < 1e-12:
        return [0.0]
    r = math.sqrt(mu)
    return [0.0, -r, r]

def classify_scalar_stability(derivative_value: float, tolerance: float = 1e-8) -> str:
    if derivative_value < -tolerance:
        return "locally_stable"
    if derivative_value > tolerance:
        return "locally_unstable"
    return "inconclusive_at_critical_value"

def saddle_node_derivative(x: float) -> float:
    return -2.0 * x

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("saddle-node-equilibria")
    p.add_argument("--mu", type=float, default=4.0)

    p = sub.add_parser("transcritical-equilibria")
    p.add_argument("--mu", type=float, default=2.0)

    p = sub.add_parser("pitchfork-equilibria")
    p.add_argument("--mu", type=float, default=4.0)

    p = sub.add_parser("classify-derivative")
    p.add_argument("--derivative-value", type=float, default=-2.0)

    p = sub.add_parser("saddle-node-sweep")
    p.add_argument("--mu-min", type=float, default=-2.0)
    p.add_argument("--mu-max", type=float, default=4.0)
    p.add_argument("--mu-step", type=float, default=0.5)

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "saddle-node-equilibria":
        eqs = saddle_node_equilibria(args.mu)
        emit(cmd, args, {"equilibria": eqs, "count": len(eqs)}, "Computes equilibria for x' = mu - x^2.", "For mu < 0, no real equilibria exist in this normal form.")
    elif cmd == "transcritical-equilibria":
        eqs = transcritical_equilibria(args.mu)
        emit(cmd, args, {"equilibria": eqs, "count": len(eqs)}, "Computes equilibria for x' = mu*x - x^2.", "Stability exchange interpretation depends on model domain.")
    elif cmd == "pitchfork-equilibria":
        eqs = pitchfork_equilibria(args.mu)
        emit(cmd, args, {"equilibria": eqs, "count": len(eqs)}, "Computes equilibria for x' = mu*x - x^3.", "Pitchfork models often assume symmetry that may not hold in real systems.")
    elif cmd == "classify-derivative":
        emit(cmd, args, {"stability": classify_scalar_stability(args.derivative_value)}, "Classifies scalar local stability from derivative sign.", "Derivative-based classification is local.")
    elif cmd == "saddle-node-sweep":
        rows = []
        steps = int(round((args.mu_max - args.mu_min) / args.mu_step))
        for i in range(steps + 1):
            mu = args.mu_min + i * args.mu_step
            eqs = saddle_node_equilibria(mu)
            if not eqs:
                rows.append({"mu": mu, "equilibrium": None, "derivative_value": None, "stability": "no_real_equilibrium", "branch_status": "equilibrium_absent"})
            else:
                for eq in eqs:
                    d = saddle_node_derivative(eq)
                    rows.append({"mu": mu, "equilibrium": eq, "derivative_value": d, "stability": classify_scalar_stability(d), "branch_status": "critical_branch" if abs(mu) < 1e-12 else "equilibrium_present"})
        write_series("saddle_node_sweep", rows)
        emit(cmd, args, {"records": len(rows)}, "Builds a saddle-node bifurcation parameter sweep.", "Sweep resolution affects critical value detection.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
