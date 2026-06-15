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

def position(t: float) -> tuple[float, float]:
    return (t, math.sin(t))

def velocity(t: float) -> tuple[float, float]:
    return (1.0, math.cos(t))

def acceleration(t: float) -> tuple[float, float]:
    return (0.0, -math.sin(t))

def distance(p: tuple[float, float], q: tuple[float, float]) -> float:
    return math.sqrt((q[0]-p[0])**2 + (q[1]-p[1])**2)

def sample_times(start: float, stop: float, step: float) -> list[float]:
    count = int((stop-start)/step)
    return [start+i*step for i in range(count+1)]

def trajectory_summary(step: float) -> dict:
    times = sample_times(0.0, 2.0*math.pi, step)
    points = [position(t) for t in times]
    segments = [distance(points[i], points[i+1]) for i in range(len(points)-1)]
    speeds = [segments[i] / (times[i+1]-times[i]) for i in range(len(segments))]
    arc = sum(segments)
    disp = distance(points[0], points[-1])
    return {
        "point_count": len(points),
        "approximate_arc_length": arc,
        "displacement_magnitude": disp,
        "path_efficiency": disp / max(arc, 1e-12),
        "average_speed": sum(speeds)/len(speeds),
        "maximum_speed": max(speeds),
    }

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    for name in ("position", "velocity", "acceleration", "speed"):
        p = sub.add_parser(name)
        p.add_argument("--t", type=float, default=1.0)

    p = sub.add_parser("distance")
    p.add_argument("--x1", type=float, default=0.0)
    p.add_argument("--y1", type=float, default=0.0)
    p.add_argument("--x2", type=float, default=3.0)
    p.add_argument("--y2", type=float, default=4.0)

    p = sub.add_parser("displacement")
    p.add_argument("--start", type=float, default=0.0)
    p.add_argument("--stop", type=float, default=2.0 * math.pi)

    for name in ("arc-length-approx", "path-efficiency", "trajectory-audit"):
        p = sub.add_parser(name)
        p.add_argument("--step", type=float, default=0.25)

    p = sub.add_parser("finite-difference-velocity")
    p.add_argument("--t", type=float, default=1.0)
    p.add_argument("--dt", type=float, default=0.01)

    return parser

def main():
    args = build_parser().parse_args()

    if args.command == "position":
        x, y = position(args.t)
        emit("position", args, {"x": x, "y": y}, "Evaluates r(t)=<t,sin(t)>.")
    elif args.command == "velocity":
        vx, vy = velocity(args.t)
        emit("velocity", args, {"vx": vx, "vy": vy}, "Evaluates r'(t)=<1,cos(t)>.")
    elif args.command == "acceleration":
        ax, ay = acceleration(args.t)
        emit("acceleration", args, {"ax": ax, "ay": ay}, "Evaluates r''(t)=<0,-sin(t)>.")
    elif args.command == "speed":
        vx, vy = velocity(args.t)
        emit("speed", args, {"speed": math.sqrt(vx*vx + vy*vy)}, "Computes the magnitude of velocity.")
    elif args.command == "distance":
        emit("distance", args, {"distance": distance((args.x1,args.y1),(args.x2,args.y2))}, "Computes distance between two points.")
    elif args.command == "displacement":
        emit("displacement", args, {"displacement_magnitude": distance(position(args.start), position(args.stop))}, "Computes net displacement magnitude.")
    elif args.command == "arc-length-approx":
        warning = "Time step is coarse." if args.step > 0.5 else ""
        emit("arc-length-approx", args, {"approximate_arc_length": trajectory_summary(args.step)["approximate_arc_length"]}, "Approximates arc length from sampled segments.", warning)
    elif args.command == "path-efficiency":
        summary = trajectory_summary(args.step)
        emit("path-efficiency", args, {"path_efficiency": summary["path_efficiency"], "displacement_magnitude": summary["displacement_magnitude"], "approximate_arc_length": summary["approximate_arc_length"]}, "Compares displacement to distance traveled.")
    elif args.command == "finite-difference-velocity":
        p0 = position(args.t)
        p1 = position(args.t + args.dt)
        emit("finite-difference-velocity", args, {"vx": (p1[0]-p0[0])/args.dt, "vy": (p1[1]-p0[1])/args.dt}, "Approximates velocity by finite difference.", "Smaller dt may reduce truncation error but amplify noise.")
    elif args.command == "trajectory-audit":
        warning = "Time step is coarse; turns and speed variation may be undersampled." if args.step > 0.5 else ""
        emit("trajectory-audit", args, trajectory_summary(args.step), "Audits a sampled vector-valued trajectory.", warning)
    else:
        raise ValueError(args.command)

if __name__ == "__main__":
    main()
