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
    return 3.0 * x + 2.0 * y + 0.5 * x * y

def gradient(x: float, y: float) -> tuple[float, float]:
    return (3.0 + 0.5 * y, 2.0 + 0.5 * x)

def normalize(vx: float, vy: float) -> tuple[float, float]:
    norm = math.sqrt(vx * vx + vy * vy)
    if norm == 0:
        raise ValueError("Direction vector must be nonzero.")
    return vx / norm, vy / norm

def directional_derivative(x: float, y: float, vx: float, vy: float) -> tuple[float, float, float]:
    ux, uy = normalize(vx, vy)
    gx, gy = gradient(x, y)
    return gx * ux + gy * uy, ux, uy

def feasible_direction(x: float, y: float, ux: float, uy: float, step: float, budget: float = 10.0) -> bool:
    return x >= 0 and y >= 0 and x + y <= budget and x + step * ux >= 0 and y + step * uy >= 0 and x + step * ux + y + step * uy <= budget

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    for name in ("evaluate", "gradient", "gradient-norm", "gradient-ascent-step", "gradient-descent-step", "compare-directions", "contour-tangent"):
        p = sub.add_parser(name)
        p.add_argument("--x", type=float, default=4)
        p.add_argument("--y", type=float, default=3)
        if name in ("gradient-ascent-step", "gradient-descent-step"):
            p.add_argument("--step", type=float, default=0.25)

    p = sub.add_parser("normalize")
    p.add_argument("--vx", type=float, default=2)
    p.add_argument("--vy", type=float, default=-1)

    for name in ("directional-derivative", "estimated-change", "feasible-direction"):
        p = sub.add_parser(name)
        p.add_argument("--x", type=float, default=4)
        p.add_argument("--y", type=float, default=3)
        p.add_argument("--vx", type=float, default=1)
        p.add_argument("--vy", type=float, default=1)
        if name in ("estimated-change", "feasible-direction"):
            p.add_argument("--step", type=float, default=0.25)
        if name == "feasible-direction":
            p.add_argument("--budget", type=float, default=10)

    return parser

def main():
    args = build_parser().parse_args()

    if args.command == "evaluate":
        emit("evaluate", args, {"output": f(args.x, args.y)}, "Evaluates the scalar function at the reference point.")
    elif args.command == "gradient":
        gx, gy = gradient(args.x, args.y)
        emit("gradient", args, {"gradient_x": gx, "gradient_y": gy}, "The gradient collects local partial sensitivities.")
    elif args.command == "gradient-norm":
        gx, gy = gradient(args.x, args.y)
        emit("gradient-norm", args, {"gradient_norm": math.sqrt(gx * gx + gy * gy)}, "The gradient norm is the maximum local rate under Euclidean scaling.")
    elif args.command == "normalize":
        ux, uy = normalize(args.vx, args.vy)
        emit("normalize", args, {"unit_x": ux, "unit_y": uy, "norm": 1.0}, "Normalizes a direction vector for rate comparison.")
    elif args.command == "directional-derivative":
        derivative, ux, uy = directional_derivative(args.x, args.y, args.vx, args.vy)
        emit("directional-derivative", args, {"unit_x": ux, "unit_y": uy, "directional_derivative": derivative}, "Computes local rate of change along a unit direction.")
    elif args.command == "estimated-change":
        derivative, ux, uy = directional_derivative(args.x, args.y, args.vx, args.vy)
        estimated = args.step * derivative
        actual = f(args.x + args.step * ux, args.y + args.step * uy) - f(args.x, args.y)
        emit("estimated-change", args, {"unit_x": ux, "unit_y": uy, "directional_derivative": derivative, "estimated_change": estimated, "actual_change": actual, "absolute_error": abs(actual - estimated)}, "Compares local directional estimate with actual finite change.")
    elif args.command == "feasible-direction":
        derivative, ux, uy = directional_derivative(args.x, args.y, args.vx, args.vy)
        feasible = feasible_direction(args.x, args.y, ux, uy, args.step, args.budget)
        emit("feasible-direction", args, {"unit_x": ux, "unit_y": uy, "directional_derivative": derivative, "feasible_direction": feasible}, "Checks whether direction and step remain in the feasible region.", "" if feasible else "Direction and step move outside the feasible region.")
    elif args.command in ("gradient-ascent-step", "gradient-descent-step"):
        gx, gy = gradient(args.x, args.y)
        sign = 1.0 if args.command == "gradient-ascent-step" else -1.0
        ux, uy = normalize(sign * gx, sign * gy)
        estimated = args.step * (gx * ux + gy * uy)
        emit(args.command, args, {"unit_x": ux, "unit_y": uy, "estimated_change": estimated, "next_x": args.x + args.step * ux, "next_y": args.y + args.step * uy}, "Computes a local step along the positive or negative gradient.")
    elif args.command == "compare-directions":
        directions = [(1,0),(0,1),(1,1),(2,-1),(-1,1)]
        rows = []
        for vx, vy in directions:
            derivative, ux, uy = directional_derivative(args.x, args.y, vx, vy)
            rows.append({"direction_x": vx, "direction_y": vy, "unit_x": ux, "unit_y": uy, "directional_derivative": derivative})
        ensure_output_dir()
        with (OUTPUT_DIR / "direction_comparison.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["direction_x","direction_y","unit_x","unit_y","directional_derivative"])
            writer.writeheader()
            writer.writerows(rows)
        best = max(rows, key=lambda r: r["directional_derivative"])
        emit("compare-directions", args, {"directions_written": len(rows), "best_directional_derivative": best["directional_derivative"], "best_direction_x": best["direction_x"], "best_direction_y": best["direction_y"]}, "Compares several scenario directions at one reference point.")
    elif args.command == "contour-tangent":
        gx, gy = gradient(args.x, args.y)
        tx, ty = normalize(-gy, gx)
        emit("contour-tangent", args, {"tangent_x": tx, "tangent_y": ty, "directional_derivative": gx * tx + gy * ty}, "Computes a direction tangent to the local contour, producing zero first-order change.")
    else:
        raise ValueError(args.command)

if __name__ == "__main__":
    main()
