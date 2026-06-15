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

def f(x: float, y: float) -> float:
    return x*x + x*y + 3*y*y + 0.2*x*x*y

def gradient(x: float, y: float) -> tuple[float, float]:
    return (2*x + y + 0.4*x*y, x + 6*y + 0.2*x*x)

def hessian(x: float, y: float) -> tuple[tuple[float, float], tuple[float, float]]:
    return ((2 + 0.4*y, 1 + 0.4*x), (1 + 0.4*x, 6.0))

def det2(H) -> float:
    return H[0][0]*H[1][1] - H[0][1]*H[1][0]

def trace2(H) -> float:
    return H[0][0] + H[1][1]

def classify(H) -> str:
    d = det2(H)
    h11 = H[0][0]
    if d > 0 and h11 > 0:
        return "positive definite"
    if d > 0 and h11 < 0:
        return "negative definite"
    if d < 0:
        return "indefinite"
    return "semidefinite or inconclusive"

def quadratic_term(H, dx: float, dy: float) -> float:
    return 0.5*(H[0][0]*dx*dx + 2*H[0][1]*dx*dy + H[1][1]*dy*dy)

def eigenvalues_2x2(H) -> tuple[float, float]:
    tr = trace2(H)
    d = det2(H)
    disc = max(0.0, tr*tr - 4*d)
    return ((tr + math.sqrt(disc))/2, (tr - math.sqrt(disc))/2)

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def add_xy(p):
    p.add_argument("--x", type=float, default=2)
    p.add_argument("--y", type=float, default=1)

def add_xy_dxdy(p):
    add_xy(p)
    p.add_argument("--dx", type=float, default=0.1)
    p.add_argument("--dy", type=float, default=-0.05)

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    for name in ("evaluate", "gradient", "hessian", "determinant", "classify", "eigen-2x2", "conditioning-check", "cross-partial"):
        add_xy(sub.add_parser(name))

    for name in ("quadratic-term", "first-order", "second-order", "approximation-error"):
        add_xy_dxdy(sub.add_parser(name))

    return parser

def main():
    args = build_parser().parse_args()
    H = hessian(args.x, args.y) if hasattr(args, "x") else None

    if args.command == "evaluate":
        emit("evaluate", args, {"output": f(args.x, args.y)}, "Evaluates the scalar function at the reference point.")
    elif args.command == "gradient":
        gx, gy = gradient(args.x, args.y)
        emit("gradient", args, {"gradient_x": gx, "gradient_y": gy}, "Computes first-order local sensitivity.")
    elif args.command == "hessian":
        emit("hessian", args, {"h11": H[0][0], "h12": H[0][1], "h21": H[1][0], "h22": H[1][1]}, "Computes the Hessian curvature matrix.")
    elif args.command == "determinant":
        d = det2(H)
        emit("determinant", args, {"determinant": d}, "Computes the Hessian determinant for two-variable curvature classification.", "" if abs(d) > 1e-8 else "Hessian is singular or nearly singular.")
    elif args.command == "classify":
        c = classify(H)
        emit("classify", args, {"classification": c, "determinant": det2(H), "trace": trace2(H)}, "Classifies local curvature using the two-variable Hessian test.", "Local classification is not global." if c != "positive definite" else "")
    elif args.command == "quadratic-term":
        q = quadratic_term(H, args.dx, args.dy)
        emit("quadratic-term", args, {"quadratic_term": q}, "Computes the second-order curvature correction.")
    elif args.command == "first-order":
        gx, gy = gradient(args.x, args.y)
        first = gx*args.dx + gy*args.dy
        emit("first-order", args, {"first_order_change": first}, "Computes the linear gradient-based change estimate.")
    elif args.command == "second-order":
        gx, gy = gradient(args.x, args.y)
        first = gx*args.dx + gy*args.dy
        second = first + quadratic_term(H, args.dx, args.dy)
        emit("second-order", args, {"first_order_change": first, "second_order_change": second}, "Computes the second-order Taylor change estimate.")
    elif args.command == "approximation-error":
        gx, gy = gradient(args.x, args.y)
        first = gx*args.dx + gy*args.dy
        second = first + quadratic_term(H, args.dx, args.dy)
        actual = f(args.x + args.dx, args.y + args.dy) - f(args.x, args.y)
        emit("approximation-error", args, {"actual_change": actual, "first_order_change": first, "second_order_change": second, "first_order_error": abs(actual-first), "second_order_error": abs(actual-second)}, "Compares first-order and second-order approximations with actual nonlinear change.")
    elif args.command == "eigen-2x2":
        l1, l2 = eigenvalues_2x2(H)
        emit("eigen-2x2", args, {"lambda_1": l1, "lambda_2": l2}, "Computes principal curvature eigenvalues for a symmetric 2x2 Hessian.")
    elif args.command == "conditioning-check":
        l1, l2 = eigenvalues_2x2(H)
        smallest = min(abs(l1), abs(l2))
        cond = math.inf if smallest == 0 else max(abs(l1), abs(l2)) / smallest
        warning = "Hessian is singular or very poorly conditioned." if (not math.isfinite(cond) or cond > 1e6) else ""
        emit("conditioning-check", args, {"condition_estimate": cond, "lambda_1": l1, "lambda_2": l2}, "Estimates curvature conditioning from eigenvalues.", warning)
    elif args.command == "cross-partial":
        emit("cross-partial", args, {"cross_partial_xy": H[0][1], "cross_partial_yx": H[1][0]}, "Reports off-diagonal Hessian entries as local second-order interaction terms.")
    else:
        raise ValueError(args.command)

if __name__ == "__main__":
    main()
