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

def path_point(t: float) -> tuple[float, float]:
    return (t, math.sin(t))

def scalar_field(x: float, y: float) -> float:
    return 1.0 + y*y

def vector_field(x: float, y: float) -> tuple[float, float]:
    return (1.0, x)

def distance(p: tuple[float,float], q: tuple[float,float]) -> float:
    return math.sqrt((q[0]-p[0])**2 + (q[1]-p[1])**2)

def dot(a: tuple[float,float], b: tuple[float,float]) -> float:
    return a[0]*b[0] + a[1]*b[1]

def sample_times(step: float) -> list[float]:
    return [i*step for i in range(int((2.0*math.pi)/step)+1)]

def line_summary(step: float) -> dict:
    pts = [path_point(t) for t in sample_times(step)]
    path_len = 0.0
    scalar_total = 0.0
    vector_total = 0.0
    alignments = []
    for i in range(len(pts)-1):
        p, q = pts[i], pts[i+1]
        disp = (q[0]-p[0], q[1]-p[1])
        seg = distance(p,q)
        field_v = vector_field(p[0],p[1])
        term = dot(field_v, disp)
        path_len += seg
        scalar_total += scalar_field(p[0],p[1]) * seg
        vector_total += term
        alignments.append(term / max(seg, 1e-12))
    return {
        "point_count": len(pts),
        "path_length": path_len,
        "scalar_line_integral": scalar_total,
        "vector_line_integral": vector_total,
        "average_alignment": sum(alignments)/len(alignments),
    }

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("path-point")
    p.add_argument("--t", type=float, default=1.0)

    for name in ("scalar-field", "vector-field"):
        p = sub.add_parser(name)
        p.add_argument("--x", type=float, default=1.0)
        p.add_argument("--y", type=float, default=2.0)

    p = sub.add_parser("segment-length")
    p.add_argument("--x1", type=float, default=0.0)
    p.add_argument("--y1", type=float, default=0.0)
    p.add_argument("--x2", type=float, default=3.0)
    p.add_argument("--y2", type=float, default=4.0)

    p = sub.add_parser("scalar-segment")
    p.add_argument("--x", type=float, default=1.0)
    p.add_argument("--y", type=float, default=2.0)
    p.add_argument("--segment-length", type=float, default=0.5)

    p = sub.add_parser("vector-segment")
    p.add_argument("--x", type=float, default=1.0)
    p.add_argument("--y", type=float, default=2.0)
    p.add_argument("--dx", type=float, default=0.25)
    p.add_argument("--dy", type=float, default=0.1)

    for name in ("line-audit", "path-length", "scalar-line-approx", "vector-line-approx"):
        p = sub.add_parser(name)
        p.add_argument("--step", type=float, default=0.25)

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "path-point":
        x, y = path_point(args.t)
        emit(cmd, args, {"x": x, "y": y}, "Evaluates the parameterized path r(t)=<t,sin(t)>.")
    elif cmd == "scalar-field":
        emit(cmd, args, {"scalar_value": scalar_field(args.x,args.y)}, "Evaluates the scalar field f(x,y)=1+y^2.")
    elif cmd == "vector-field":
        vx, vy = vector_field(args.x,args.y)
        emit(cmd, args, {"vx": vx, "vy": vy}, "Evaluates the vector field F(x,y)=<1,x>.")
    elif cmd == "segment-length":
        emit(cmd, args, {"segment_length": distance((args.x1,args.y1),(args.x2,args.y2))}, "Computes length of a path segment.")
    elif cmd == "scalar-segment":
        emit(cmd, args, {"contribution": scalar_field(args.x,args.y) * args.segment_length}, "Computes one scalar line-integral segment contribution.")
    elif cmd == "vector-segment":
        vx, vy = vector_field(args.x,args.y)
        emit(cmd, args, {"contribution": dot((vx,vy),(args.dx,args.dy))}, "Computes one vector line-integral dot-product segment contribution.")
    elif cmd == "line-audit":
        warning = "Time step is coarse." if args.step > 0.5 else ""
        emit(cmd, args, line_summary(args.step), "Audits scalar and vector line-integral approximations.", warning)
    elif cmd == "path-length":
        emit(cmd, args, {"path_length": line_summary(args.step)["path_length"]}, "Approximates path length by segment sampling.")
    elif cmd == "scalar-line-approx":
        emit(cmd, args, {"scalar_line_integral": line_summary(args.step)["scalar_line_integral"]}, "Approximates scalar line integral along the path.")
    elif cmd == "vector-line-approx":
        emit(cmd, args, {"vector_line_integral": line_summary(args.step)["vector_line_integral"]}, "Approximates vector line integral along the directed path.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
