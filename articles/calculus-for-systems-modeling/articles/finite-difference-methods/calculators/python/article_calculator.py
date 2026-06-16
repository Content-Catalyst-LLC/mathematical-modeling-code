#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json
from pathlib import Path
OUT = Path(__file__).resolve().parents[1] / "outputs"

def save(name, payload):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{name}.json").write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    flat = {"calculator": payload["calculator"]}
    flat.update(payload.get("result", {}))
    with (OUT / f"{name}.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(flat.keys()))
        w.writeheader()
        w.writerow(flat)

def ratio(diffusivity, dt, dx): return diffusivity * dt / (dx * dx)
def step(left, center, right, r): return center + r * (right - 2 * center + left)

parser = argparse.ArgumentParser()
sub = parser.add_subparsers(dest="command", required=True)
p=sub.add_parser("diffusion-ratio"); p.add_argument("--diffusivity", type=float, default=0.08); p.add_argument("--dt", type=float, default=0.2); p.add_argument("--dx", type=float, default=1.0)
p=sub.add_parser("forward-difference"); p.add_argument("--f-current", type=float, default=1.0); p.add_argument("--f-next", type=float, default=1.2); p.add_argument("--dx", type=float, default=0.1)
p=sub.add_parser("central-difference"); p.add_argument("--f-previous", type=float, default=1.0); p.add_argument("--f-next", type=float, default=1.2); p.add_argument("--dx", type=float, default=0.1)
p=sub.add_parser("second-central-difference"); p.add_argument("--f-previous", type=float, default=1.0); p.add_argument("--f-current", type=float, default=1.2); p.add_argument("--f-next", type=float, default=1.4); p.add_argument("--dx", type=float, default=0.1)
p=sub.add_parser("explicit-diffusion-step"); p.add_argument("--left", type=float, default=0.0); p.add_argument("--center", type=float, default=1.0); p.add_argument("--right", type=float, default=0.0); p.add_argument("--ratio", type=float, default=0.016)
p=sub.add_parser("stability-check"); p.add_argument("--diffusivity", type=float, default=0.08); p.add_argument("--dt", type=float, default=0.2); p.add_argument("--dx", type=float, default=1.0)
p=sub.add_parser("diffusion-simulation"); p.add_argument("--grid-points", type=int, default=61); p.add_argument("--diffusivity", type=float, default=0.08); p.add_argument("--dx", type=float, default=1.0); p.add_argument("--dt", type=float, default=0.2); p.add_argument("--steps", type=int, default=120)
args = parser.parse_args()
cmd = args.command

if cmd == "diffusion-ratio":
    result = {"diffusion_ratio": ratio(args.diffusivity, args.dt, args.dx)}
elif cmd == "forward-difference":
    result = {"derivative_estimate": (args.f_next - args.f_current) / args.dx}
elif cmd == "central-difference":
    result = {"derivative_estimate": (args.f_next - args.f_previous) / (2 * args.dx)}
elif cmd == "second-central-difference":
    result = {"second_derivative_estimate": (args.f_next - 2 * args.f_current + args.f_previous) / (args.dx * args.dx)}
elif cmd == "explicit-diffusion-step":
    result = {"updated_center": step(args.left, args.center, args.right, args.ratio)}
elif cmd == "stability-check":
    r = ratio(args.diffusivity, args.dt, args.dx)
    result = {"diffusion_ratio": r, "stability_status": "stable_for_basic_explicit_1d_diffusion" if r <= 0.5 else "unstable_risk"}
elif cmd == "diffusion-simulation":
    r = ratio(args.diffusivity, args.dt, args.dx)
    status = "stable_for_basic_explicit_1d_diffusion" if r <= 0.5 else "unstable_risk"
    field = [0.0 for _ in range(args.grid_points)]
    field[args.grid_points // 2] = 1.0
    rows = []
    for n in range(args.steps + 1):
        rows.append({"step": n, "time": n * args.dt, "center_value": field[args.grid_points // 2], "total_mass": sum(field) * args.dx, "max_value": max(field), "diffusion_ratio": r, "stability_status": status})
        updated = field[:]
        for i in range(1, args.grid_points - 1):
            updated[i] = step(field[i-1], field[i], field[i+1], r)
        updated[0] = 0.0
        updated[-1] = 0.0
        field = updated
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "diffusion_simulation.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    with (OUT / "diffusion_simulation.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    result = {"records": len(rows), "final_center_value": rows[-1]["center_value"], "diffusion_ratio": r, "stability_status": status}
else:
    raise ValueError(cmd)

payload = {"calculator": cmd, "inputs": vars(args), "result": result, "warning": "Finite difference outputs depend on grid spacing, time step, stencil, boundary condition, stability, and convergence checks."}
save(cmd.replace("-", "_"), payload)
print(json.dumps(payload, indent=2, sort_keys=True))
