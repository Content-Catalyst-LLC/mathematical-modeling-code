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

def vector_field(x: float, y: float) -> tuple[float, float]:
    return (-y, x)

def dot(a: tuple[float, float], b: tuple[float, float]) -> float:
    return a[0]*b[0] + a[1]*b[1]

def segment_geometry(radius: float, segments: int, index: int) -> dict:
    i = index % segments
    theta0 = 2*math.pi*i/segments
    theta1 = 2*math.pi*(i+1)/segments
    x0, y0 = radius*math.cos(theta0), radius*math.sin(theta0)
    x1, y1 = radius*math.cos(theta1), radius*math.sin(theta1)
    xm, ym = 0.5*(x0+x1), 0.5*(y0+y1)
    dx, dy = x1-x0, y1-y0
    segment_length = math.sqrt(dx*dx + dy*dy)
    return {
        "midpoint": (xm, ym),
        "segment": (dx, dy),
        "segment_length": segment_length,
        "tangent": (dx/segment_length, dy/segment_length),
        "normal": (xm/radius, ym/radius),
    }

def circle_summary(radius: float, segments: int) -> dict:
    flux = 0.0
    circulation = 0.0
    tangential = []
    normal = []
    for i in range(segments):
        geom = segment_geometry(radius, segments, i)
        field = vector_field(*geom["midpoint"])
        flux += dot(field, geom["normal"]) * geom["segment_length"]
        circulation += dot(field, geom["segment"])
        tangential.append(dot(field, geom["tangent"]))
        normal.append(dot(field, geom["normal"]))
    return {
        "approximate_flux": flux,
        "approximate_circulation": circulation,
        "mean_tangential_alignment": sum(tangential)/len(tangential),
        "mean_normal_alignment": sum(normal)/len(normal),
        "segment_count": segments,
    }

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("vector-field")
    p.add_argument("--x", type=float, default=1.0)
    p.add_argument("--y", type=float, default=0.0)

    for name in ("normal-alignment", "tangent-alignment"):
        p = sub.add_parser(name)
        p.add_argument("--x", type=float, default=1.0)
        p.add_argument("--y", type=float, default=0.0)

    for name in ("flux-segment", "circulation-segment"):
        p = sub.add_parser(name)
        p.add_argument("--radius", type=float, default=1.0)
        p.add_argument("--segments", type=int, default=64)
        p.add_argument("--index", type=int, default=0)

    for name in ("circle-flux", "circle-circulation", "flow-audit"):
        p = sub.add_parser(name)
        p.add_argument("--radius", type=float, default=1.0)
        p.add_argument("--segments", type=int, default=64)

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "vector-field":
        fx, fy = vector_field(args.x, args.y)
        emit(cmd, args, {"fx": fx, "fy": fy}, "Evaluates rotating vector field F=<-y,x>.")
    elif cmd == "normal-alignment":
        radius = math.sqrt(args.x*args.x + args.y*args.y) or 1.0
        field = vector_field(args.x, args.y)
        normal = (args.x/radius, args.y/radius)
        emit(cmd, args, {"normal_alignment": dot(field, normal)}, "Measures field alignment with outward radial normal.")
    elif cmd == "tangent-alignment":
        radius = math.sqrt(args.x*args.x + args.y*args.y) or 1.0
        field = vector_field(args.x, args.y)
        tangent = (-args.y/radius, args.x/radius)
        emit(cmd, args, {"tangent_alignment": dot(field, tangent)}, "Measures field alignment with counterclockwise tangent.")
    elif cmd == "flux-segment":
        geom = segment_geometry(args.radius, args.segments, args.index)
        field = vector_field(*geom["midpoint"])
        value = dot(field, geom["normal"]) * geom["segment_length"]
        emit(cmd, args, {"flux_segment": value}, "Computes one segment contribution to outward flux.")
    elif cmd == "circulation-segment":
        geom = segment_geometry(args.radius, args.segments, args.index)
        field = vector_field(*geom["midpoint"])
        value = dot(field, geom["segment"])
        emit(cmd, args, {"circulation_segment": value}, "Computes one segment contribution to circulation.")
    elif cmd == "circle-flux":
        emit(cmd, args, {"approximate_flux": circle_summary(args.radius,args.segments)["approximate_flux"]}, "Approximates outward flux through a circular boundary.")
    elif cmd == "circle-circulation":
        emit(cmd, args, {"approximate_circulation": circle_summary(args.radius,args.segments)["approximate_circulation"]}, "Approximates circulation around a circular path.")
    elif cmd == "flow-audit":
        warning = "Coarse path sampling." if args.segments < 32 else ""
        emit(cmd, args, circle_summary(args.radius,args.segments), "Audits flux, circulation, tangent alignment, and normal alignment.", warning)
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
