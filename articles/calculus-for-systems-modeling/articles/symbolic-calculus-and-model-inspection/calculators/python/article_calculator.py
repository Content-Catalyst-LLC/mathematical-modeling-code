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

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("logistic-derivative")
    sub.add_parser("logistic-equilibria")
    sub.add_parser("capacity-limit")
    sub.add_parser("jacobian-record")
    p = sub.add_parser("domain-warning")
    p.add_argument("--expression", default="r*x*(1 - x/K)")
    sub.add_parser("symbolic-inspection-report")
    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "logistic-derivative":
        emit(cmd, args, {"rate_expression": "r*x*(1 - x/K)", "first_derivative": "r - 2*r*x/K", "second_derivative": "-2*r/K"}, "Returns symbolic derivative records for logistic growth.", "Derivative signs depend on parameter regimes and domain assumptions.")
    elif cmd == "logistic-equilibria":
        emit(cmd, args, {"equilibria": "x = 0 or x = K"}, "Returns candidate equilibria for the logistic rate expression.", "Equilibria require domain and stability review.")
    elif cmd == "capacity-limit":
        emit(cmd, args, {"limit_as_x_approaches_K": "0"}, "Returns boundary behavior at carrying capacity.", "Boundary behavior should be checked against modeled assumptions.")
    elif cmd == "jacobian-record":
        emit(cmd, args, {"jacobian": "[r - 2*r*x/K]"}, "Returns a one-state Jacobian record.", "Local linear inspection does not replace nonlinear simulation.")
    elif cmd == "domain-warning":
        warning = "Document K as nonzero, record positivity assumptions, and preserve excluded values." if "K" in args.expression else "Document variable and parameter domains."
        emit(cmd, args, {"domain_warning": warning}, "Creates a domain and assumption warning for an expression.", "Symbolic simplification can hide excluded cases.")
    elif cmd == "symbolic-inspection-report":
        emit(cmd, args, {"records": 6, "includes": "expression, derivatives, equilibria, limit, Jacobian, domain warnings"}, "Creates a compact symbolic inspection report record.", "Exact expressions do not make a model empirically valid.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
