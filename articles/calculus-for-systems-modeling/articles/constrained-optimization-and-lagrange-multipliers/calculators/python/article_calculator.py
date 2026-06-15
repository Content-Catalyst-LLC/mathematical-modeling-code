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
    flat.update({f"input_{k}": v for k, v in payload.inputs.items()})
    flat.update({f"result_{k}": v for k, v in payload.result.items() if not isinstance(v, (list, dict))})
    with (OUTPUT_DIR / f"{name}.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(flat.keys()))
        writer.writeheader()
        writer.writerow(flat)

def objective(x: float, y: float) -> float:
    return x*x + 2*y*y

def constraint(x: float, y: float) -> float:
    return x + y

def grad_objective(x: float, y: float) -> tuple[float, float]:
    return (2*x, 4*y)

def grad_constraint(x: float, y: float) -> tuple[float, float]:
    return (1.0, 1.0)

def solve(target: float) -> tuple[float, float, float]:
    y = target / 3.0
    x = 2.0 * target / 3.0
    return x, y, 2.0*x

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("solve")
    p.add_argument("--target", type=float, default=12)

    p = sub.add_parser("objective")
    p.add_argument("--x", type=float, default=8)
    p.add_argument("--y", type=float, default=4)

    for name in ("constraint", "feasibility"):
        p = sub.add_parser(name)
        p.add_argument("--x", type=float, default=8)
        p.add_argument("--y", type=float, default=4)
        p.add_argument("--target", type=float, default=12)

    p = sub.add_parser("gradients")
    p.add_argument("--x", type=float, default=8)
    p.add_argument("--y", type=float, default=4)

    for name in ("stationarity", "multiplier"):
        p = sub.add_parser(name)
        p.add_argument("--target", type=float, default=12)

    p = sub.add_parser("shadow-value")
    p.add_argument("--target", type=float, default=12)
    p.add_argument("--delta", type=float, default=0.1)

    p = sub.add_parser("active-status")
    p.add_argument("--value", type=float, default=12)
    p.add_argument("--limit", type=float, default=12)
    p.add_argument("--tolerance", type=float, default=1e-9)

    p = sub.add_parser("tradeoff-scan")
    p.add_argument("--targets", type=float, nargs="+", default=[12, 18, 24])

    return parser

def stationarity(target: float) -> dict:
    x, y, lam = solve(target)
    gf = grad_objective(x, y)
    gg = grad_constraint(x, y)
    sx = gf[0] - lam*gg[0]
    sy = gf[1] - lam*gg[1]
    return {"x": x, "y": y, "lambda_value": lam, "stationarity_residual_norm": math.sqrt(sx*sx + sy*sy)}

def main():
    args = build_parser().parse_args()

    if args.command == "solve":
        x, y, lam = solve(args.target)
        emit("solve", args, {"x": x, "y": y, "lambda_value": lam, "objective_value": objective(x,y)}, "Solves the teaching equality-constrained problem.")
    elif args.command == "objective":
        emit("objective", args, {"objective_value": objective(args.x,args.y)}, "Evaluates the objective function.")
    elif args.command == "constraint":
        cval = constraint(args.x,args.y)
        emit("constraint", args, {"constraint_value": cval, "constraint_residual": cval - args.target}, "Computes the equality constraint residual.")
    elif args.command == "gradients":
        gf = grad_objective(args.x,args.y); gg = grad_constraint(args.x,args.y)
        emit("gradients", args, {"gradient_f_x": gf[0], "gradient_f_y": gf[1], "gradient_g_x": gg[0], "gradient_g_y": gg[1]}, "Computes objective and constraint gradients.")
    elif args.command == "stationarity":
        emit("stationarity", args, stationarity(args.target), "Computes the Lagrange stationarity residual.")
    elif args.command == "multiplier":
        x, y, lam = solve(args.target)
        emit("multiplier", args, {"lambda_value": lam, "x": x, "y": y}, "Computes the Lagrange multiplier for the teaching problem.", "Multiplier interpretation is local and unit-dependent.")
    elif args.command == "shadow-value":
        x, y, lam = solve(args.target)
        x2, y2, _ = solve(args.target + args.delta)
        exact_change = objective(x2,y2) - objective(x,y)
        emit("shadow-value", args, {"lambda_value": lam, "linear_shadow_estimate": lam*args.delta, "exact_objective_change": exact_change}, "Compares multiplier-based local shadow estimate with exact small target change.", "Shadow-value interpretation is local.")
    elif args.command == "feasibility":
        cval = constraint(args.x,args.y)
        residual = cval - args.target
        emit("feasibility", args, {"constraint_value": cval, "constraint_residual": residual, "feasible": abs(residual) <= 1e-9}, "Checks whether a point satisfies the equality constraint.")
    elif args.command == "active-status":
        residual = args.value - args.limit
        if abs(residual) <= args.tolerance:
            status = "active"
        elif residual < 0:
            status = "inactive"
        else:
            status = "violated"
        emit("active-status", args, {"residual": residual, "status": status}, "Classifies inequality boundary status.")
    elif args.command == "tradeoff-scan":
        rows = []
        for target in args.targets:
            x, y, lam = solve(target)
            rows.append({"target": target, "x": x, "y": y, "lambda_value": lam, "objective_value": objective(x,y)})
        emit("tradeoff-scan", args, {"scan": rows, "cases": len(rows)}, "Scans optimized values across constraint targets.", "Scan is synthetic and local to the example structure.")
    else:
        raise ValueError(args.command)

if __name__ == "__main__":
    main()
