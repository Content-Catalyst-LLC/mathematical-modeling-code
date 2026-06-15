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

def vector_field(x: float, y: float, z: float = 0.0) -> tuple[float, float, float]:
    return (-y, x, 0.0)

def curl_field(x: float, y: float, z: float = 0.0) -> tuple[float, float, float]:
    return (0.0, 0.0, 2.0)

def dot(a, b) -> float:
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def boundary_circulation(radius: float, segments: int) -> float:
    total = 0.0
    for i in range(segments):
        theta0 = 2*math.pi*i/segments
        theta1 = 2*math.pi*(i+1)/segments
        x0, y0 = radius*math.cos(theta0), radius*math.sin(theta0)
        x1, y1 = radius*math.cos(theta1), radius*math.sin(theta1)
        xm, ym = 0.5*(x0+x1), 0.5*(y0+y1)
        dx, dy = x1-x0, y1-y0
        total += dot(vector_field(xm, ym), (dx, dy, 0.0))
    return total

def surface_curl_flux(radius: float, radial_steps: int) -> float:
    total = 0.0
    normal = (0.0, 0.0, 1.0)
    for i in range(radial_steps):
        r0 = radius*i/radial_steps
        r1 = radius*(i+1)/radial_steps
        ring_area = math.pi*(r1*r1 - r0*r0)
        total += dot(curl_field(0.0, 0.0, 0.0), normal)*ring_area
    return total

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    for name in ("vector-field", "curl-field"):
        p = sub.add_parser(name)
        p.add_argument("--x", type=float, default=1.0)
        p.add_argument("--y", type=float, default=0.0)
        p.add_argument("--z", type=float, default=0.0)

    p = sub.add_parser("boundary-circulation")
    p.add_argument("--radius", type=float, default=1.0)
    p.add_argument("--segments", type=int, default=128)

    p = sub.add_parser("surface-curl-flux")
    p.add_argument("--radius", type=float, default=1.0)
    p.add_argument("--radial-steps", type=int, default=32)

    p = sub.add_parser("stokes-audit")
    p.add_argument("--radius", type=float, default=1.0)
    p.add_argument("--segments", type=int, default=128)
    p.add_argument("--radial-steps", type=int, default=32)

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "vector-field":
        fx, fy, fz = vector_field(args.x, args.y, args.z)
        emit(cmd, args, {"fx": fx, "fy": fy, "fz": fz}, "Evaluates F=<-y,x,0>.")
    elif cmd == "curl-field":
        cx, cy, cz = curl_field(args.x, args.y, args.z)
        emit(cmd, args, {"curl_x": cx, "curl_y": cy, "curl_z": cz}, "Evaluates curl F=<0,0,2>.")
    elif cmd == "boundary-circulation":
        emit(cmd, args, {"boundary_circulation": boundary_circulation(args.radius, args.segments)}, "Approximates boundary circulation around a circle.")
    elif cmd == "surface-curl-flux":
        emit(cmd, args, {"surface_curl_flux": surface_curl_flux(args.radius, args.radial_steps)}, "Approximates curl flux through an upward-oriented disk.")
    elif cmd == "stokes-audit":
        bc = boundary_circulation(args.radius, args.segments)
        sf = surface_curl_flux(args.radius, args.radial_steps)
        warning = "Coarse boundary or surface sampling." if args.segments < 64 or args.radial_steps < 16 else ""
        emit(cmd, args, {"boundary_circulation": bc, "surface_curl_flux": sf, "absolute_gap": abs(bc-sf)}, "Compares Stokes theorem boundary and surface quantities.", warning)
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
