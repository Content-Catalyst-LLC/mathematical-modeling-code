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
    return 20.0 + 2.0 * math.sin(x) + 0.5 * y * y

def vector_field(x: float, y: float) -> tuple[float, float]:
    return (-y, x)

def magnitude(vx: float, vy: float) -> float:
    return math.sqrt(vx*vx + vy*vy)

def grid_values(step: float) -> list[float]:
    return [round(-3.0 + i*step, 10) for i in range(int(6.0 / step) + 1)]

def grid_audit(step: float) -> dict:
    scalars = []
    mags = []
    for x in grid_values(step):
        for y in grid_values(step):
            scalars.append(scalar_field(x,y))
            vx, vy = vector_field(x,y)
            mags.append(magnitude(vx,vy))
    return {
        "point_count": len(scalars),
        "scalar_average": sum(scalars)/len(scalars),
        "scalar_minimum": min(scalars),
        "scalar_maximum": max(scalars),
        "vector_magnitude_average": sum(mags)/len(mags),
        "vector_magnitude_maximum": max(mags),
    }

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("vector-magnitude")
    p.add_argument("--vx", type=float, default=3)
    p.add_argument("--vy", type=float, default=4)

    p = sub.add_parser("vector-components")
    p.add_argument("--magnitude", type=float, default=5)
    p.add_argument("--angle-degrees", type=float, default=53.130102354)

    p = sub.add_parser("dot-product")
    p.add_argument("--ax", type=float, default=1)
    p.add_argument("--ay", type=float, default=2)
    p.add_argument("--bx", type=float, default=3)
    p.add_argument("--by", type=float, default=4)

    for name in ("scalar-field", "vector-field", "field-magnitude"):
        p = sub.add_parser(name)
        p.add_argument("--x", type=float, default=1)
        p.add_argument("--y", type=float, default=2)

    p = sub.add_parser("grid-audit")
    p.add_argument("--step", type=float, default=0.5)

    p = sub.add_parser("resolution-scan")
    p.add_argument("--steps", type=float, nargs="+", default=[1.0, 0.5, 0.25])

    p = sub.add_parser("unit-vector")
    p.add_argument("--vx", type=float, default=3)
    p.add_argument("--vy", type=float, default=4)

    p = sub.add_parser("projection")
    p.add_argument("--ax", type=float, default=3)
    p.add_argument("--ay", type=float, default=4)
    p.add_argument("--bx", type=float, default=1)
    p.add_argument("--by", type=float, default=0)

    return parser

def main():
    args = build_parser().parse_args()

    if args.command == "vector-magnitude":
        emit("vector-magnitude", args, {"magnitude": magnitude(args.vx, args.vy)}, "Computes vector magnitude from components.")
    elif args.command == "vector-components":
        theta = math.radians(args.angle_degrees)
        emit("vector-components", args, {"vx": args.magnitude * math.cos(theta), "vy": args.magnitude * math.sin(theta)}, "Computes vector components from magnitude and angle.")
    elif args.command == "dot-product":
        dot = args.ax*args.bx + args.ay*args.by
        emit("dot-product", args, {"dot_product": dot}, "Measures directional alignment between two vectors.")
    elif args.command == "scalar-field":
        emit("scalar-field", args, {"scalar_value": scalar_field(args.x, args.y)}, "Evaluates the synthetic scalar field.")
    elif args.command == "vector-field":
        vx, vy = vector_field(args.x, args.y)
        emit("vector-field", args, {"vx": vx, "vy": vy}, "Evaluates the synthetic vector field.")
    elif args.command == "field-magnitude":
        vx, vy = vector_field(args.x, args.y)
        emit("field-magnitude", args, {"vx": vx, "vy": vy, "magnitude": magnitude(vx, vy)}, "Computes vector-field magnitude at a point.")
    elif args.command == "grid-audit":
        warning = "Grid resolution is coarse; field structure may be undersampled." if args.step > 0.75 else ""
        emit("grid-audit", args, grid_audit(args.step), "Audits scalar and vector values across a grid.", warning)
    elif args.command == "resolution-scan":
        rows = [{"step": step, **grid_audit(step)} for step in args.steps]
        emit("resolution-scan", args, {"cases": len(rows), "scan": rows}, "Scans field diagnostics across grid resolutions.", "Resolution can change field summaries.")
    elif args.command == "unit-vector":
        mag = magnitude(args.vx, args.vy)
        if mag == 0:
            emit("unit-vector", args, {"ux": None, "uy": None, "magnitude": mag}, "Cannot compute unit vector for zero vector.", "Zero vector has no direction.")
        else:
            emit("unit-vector", args, {"ux": args.vx/mag, "uy": args.vy/mag, "magnitude": mag}, "Computes a unit vector in the same direction.")
    elif args.command == "projection":
        denom = args.bx*args.bx + args.by*args.by
        if denom == 0:
            emit("projection", args, {"projection_x": None, "projection_y": None}, "Cannot project onto zero vector.", "Zero target vector has no direction.")
        else:
            scale = (args.ax*args.bx + args.ay*args.by) / denom
            emit("projection", args, {"projection_x": scale*args.bx, "projection_y": scale*args.by, "scale": scale}, "Projects vector a onto vector b.")
    else:
        raise ValueError(args.command)

if __name__ == "__main__":
    main()
