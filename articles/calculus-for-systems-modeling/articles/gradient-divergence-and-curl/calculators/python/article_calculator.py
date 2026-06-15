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

def scalar_field(x: float, y: float) -> float:
    return x*x + y*y

def vector_field(x: float, y: float) -> tuple[float, float]:
    return (-y, x)

def gradient(x: float, y: float) -> tuple[float, float]:
    return (2.0*x, 2.0*y)

def gradient_magnitude(x: float, y: float) -> float:
    gx, gy = gradient(x,y)
    return math.sqrt(gx*gx + gy*gy)

def divergence(x: float, y: float) -> float:
    return 0.0

def curl_2d(x: float, y: float) -> float:
    return 2.0

def fd_gradient(x: float, y: float, h: float) -> tuple[float, float]:
    dfdx = (scalar_field(x+h,y) - scalar_field(x-h,y)) / (2*h)
    dfdy = (scalar_field(x,y+h) - scalar_field(x,y-h)) / (2*h)
    return dfdx, dfdy

def fd_divergence(x: float, y: float, h: float) -> float:
    px_plus, _ = vector_field(x+h, y)
    px_minus, _ = vector_field(x-h, y)
    _, qy_plus = vector_field(x, y+h)
    _, qy_minus = vector_field(x, y-h)
    return (px_plus - px_minus)/(2*h) + (qy_plus - qy_minus)/(2*h)

def fd_curl(x: float, y: float, h: float) -> float:
    _, qx_plus = vector_field(x+h, y)
    _, qx_minus = vector_field(x-h, y)
    py_plus, _ = vector_field(x, y+h)
    py_minus, _ = vector_field(x, y-h)
    return (qx_plus - qx_minus)/(2*h) - (py_plus - py_minus)/(2*h)

def grid_values(step: float) -> list[float]:
    return [round(-1.0 + i*step, 10) for i in range(int(2.0/step) + 1)]

def field_summary(step: float) -> dict:
    values = grid_values(step)
    grads = []
    divs = []
    curls = []
    for x in values:
        for y in values:
            grads.append(gradient_magnitude(x,y))
            divs.append(divergence(x,y))
            curls.append(curl_2d(x,y))
    return {
        "point_count": len(values)*len(values),
        "mean_gradient_magnitude": sum(grads)/len(grads),
        "maximum_gradient_magnitude": max(grads),
        "mean_divergence": sum(divs)/len(divs),
        "mean_curl": sum(curls)/len(curls),
        "maximum_abs_curl": max(abs(v) for v in curls),
    }

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    for name in ("scalar-field", "vector-field", "gradient", "gradient-magnitude", "divergence", "curl-2d"):
        p = sub.add_parser(name)
        p.add_argument("--x", type=float, default=1.0)
        p.add_argument("--y", type=float, default=1.0)

    for name in ("finite-difference-gradient", "finite-difference-divergence", "finite-difference-curl"):
        p = sub.add_parser(name)
        p.add_argument("--x", type=float, default=1.0)
        p.add_argument("--y", type=float, default=1.0)
        p.add_argument("--h", type=float, default=0.01)

    p = sub.add_parser("field-audit")
    p.add_argument("--step", type=float, default=0.25)

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "scalar-field":
        emit(cmd, args, {"value": scalar_field(args.x,args.y)}, "Evaluates scalar field f=x^2+y^2.")
    elif cmd == "vector-field":
        p, q = vector_field(args.x,args.y)
        emit(cmd, args, {"P": p, "Q": q}, "Evaluates vector field F=<-y,x>.")
    elif cmd == "gradient":
        gx, gy = gradient(args.x,args.y)
        emit(cmd, args, {"df_dx": gx, "df_dy": gy}, "Computes analytic gradient of f=x^2+y^2.")
    elif cmd == "gradient-magnitude":
        emit(cmd, args, {"gradient_magnitude": gradient_magnitude(args.x,args.y)}, "Computes gradient magnitude.")
    elif cmd == "divergence":
        emit(cmd, args, {"divergence": divergence(args.x,args.y)}, "Computes analytic divergence of F=<-y,x>.")
    elif cmd == "curl-2d":
        emit(cmd, args, {"curl_2d": curl_2d(args.x,args.y)}, "Computes 2D curl scalar of F=<-y,x>.")
    elif cmd == "finite-difference-gradient":
        gx, gy = fd_gradient(args.x,args.y,args.h)
        emit(cmd, args, {"df_dx": gx, "df_dy": gy}, "Approximates gradient by central differences.", "" if args.h > 0 else "h must be positive.")
    elif cmd == "finite-difference-divergence":
        emit(cmd, args, {"divergence": fd_divergence(args.x,args.y,args.h)}, "Approximates divergence by central differences.", "" if args.h > 0 else "h must be positive.")
    elif cmd == "finite-difference-curl":
        emit(cmd, args, {"curl_2d": fd_curl(args.x,args.y,args.h)}, "Approximates 2D curl by central differences.", "" if args.h > 0 else "h must be positive.")
    elif cmd == "field-audit":
        warning = "Grid step is coarse." if args.step > 0.5 else ""
        emit(cmd, args, field_summary(args.step), "Audits gradient, divergence, and curl across a grid.", warning)
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
