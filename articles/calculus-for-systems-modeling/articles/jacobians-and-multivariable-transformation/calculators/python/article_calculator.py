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

def F(x: float, y: float) -> tuple[float, float]:
    return (x * x + y, x * y + 3.0 * y)

def J(x: float, y: float) -> tuple[tuple[float, float], tuple[float, float]]:
    return ((2.0 * x, 1.0), (y, x + 3.0))

def det2(M) -> float:
    return M[0][0] * M[1][1] - M[0][1] * M[1][0]

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    for name in ("evaluate", "jacobian", "determinant", "singularity-check"):
        p = sub.add_parser(name)
        p.add_argument("--x", type=float, default=2)
        p.add_argument("--y", type=float, default=1)

    for name in ("local-linear", "approximation-error"):
        p = sub.add_parser(name)
        p.add_argument("--x", type=float, default=2)
        p.add_argument("--y", type=float, default=1)
        p.add_argument("--dx", type=float, default=0.1)
        p.add_argument("--dy", type=float, default=-0.05)

    p = sub.add_parser("area-scaling")
    p.add_argument("--x", type=float, default=2)
    p.add_argument("--y", type=float, default=1)
    p.add_argument("--area", type=float, default=3)

    p = sub.add_parser("polar-jacobian")
    p.add_argument("--r", type=float, default=3)
    p.add_argument("--theta", type=float, default=0.785398163)

    p = sub.add_parser("sensitivity-column")
    p.add_argument("--x", type=float, default=2)
    p.add_argument("--y", type=float, default=1)
    p.add_argument("--input-index", type=int, default=1, choices=[1,2])

    p = sub.add_parser("sensitivity-row")
    p.add_argument("--x", type=float, default=2)
    p.add_argument("--y", type=float, default=1)
    p.add_argument("--output-index", type=int, default=1, choices=[1,2])

    return parser

def main():
    args = build_parser().parse_args()

    if args.command == "evaluate":
        o1, o2 = F(args.x, args.y)
        emit("evaluate", args, {"output_1": o1, "output_2": o2}, "Evaluates the vector-valued transformation.")
    elif args.command == "jacobian":
        M = J(args.x, args.y)
        emit("jacobian", args, {"j11": M[0][0], "j12": M[0][1], "j21": M[1][0], "j22": M[1][1]}, "Computes the local Jacobian matrix.")
    elif args.command == "determinant":
        M = J(args.x, args.y)
        d = det2(M)
        emit("determinant", args, {"determinant": d, "absolute_determinant": abs(d)}, "Computes local signed and absolute area scaling.", "" if abs(d) > 1e-8 else "Jacobian is singular or near singular.")
    elif args.command in ("local-linear", "approximation-error"):
        M = J(args.x, args.y)
        baseline = F(args.x, args.y)
        actual = F(args.x + args.dx, args.y + args.dy)
        approx_change = (M[0][0] * args.dx + M[0][1] * args.dy, M[1][0] * args.dx + M[1][1] * args.dy)
        actual_change = (actual[0] - baseline[0], actual[1] - baseline[1])
        err = math.sqrt((actual_change[0] - approx_change[0])**2 + (actual_change[1] - approx_change[1])**2)
        emit(args.command, args, {"approximate_change_1": approx_change[0], "approximate_change_2": approx_change[1], "actual_change_1": actual_change[0], "actual_change_2": actual_change[1], "error_norm": err}, "Compares Jacobian-based local linear approximation with actual nonlinear change.")
    elif args.command == "area-scaling":
        M = J(args.x, args.y)
        d = det2(M)
        emit("area-scaling", args, {"input_area": args.area, "scaled_area": abs(d) * args.area, "absolute_determinant": abs(d)}, "Scales a small input area by the absolute determinant.")
    elif args.command == "singularity-check":
        M = J(args.x, args.y)
        d = det2(M)
        emit("singularity-check", args, {"determinant": d, "singular_or_near_singular": abs(d) <= 1e-8}, "Flags whether a square Jacobian is singular or near singular.", "" if abs(d) > 1e-8 else "Jacobian is singular or near singular.")
    elif args.command == "polar-jacobian":
        r, theta = args.r, args.theta
        emit("polar-jacobian", args, {"j11": math.cos(theta), "j12": -r * math.sin(theta), "j21": math.sin(theta), "j22": r * math.cos(theta), "determinant": r}, "Computes the polar-to-Cartesian Jacobian and area scaling factor.")
    elif args.command == "sensitivity-column":
        M = J(args.x, args.y)
        idx = args.input_index - 1
        emit("sensitivity-column", args, {"component_1": M[0][idx], "component_2": M[1][idx]}, "Returns one input column: the local effect of one input across outputs.")
    elif args.command == "sensitivity-row":
        M = J(args.x, args.y)
        idx = args.output_index - 1
        emit("sensitivity-row", args, {"input_1_sensitivity": M[idx][0], "input_2_sensitivity": M[idx][1]}, "Returns one output row: the local sensitivity of one output across inputs.")
    else:
        raise ValueError(args.command)

if __name__ == "__main__":
    main()
