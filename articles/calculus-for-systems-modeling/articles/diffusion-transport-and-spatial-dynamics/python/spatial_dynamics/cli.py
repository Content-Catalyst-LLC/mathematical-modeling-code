from __future__ import annotations
import argparse, csv, json
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class SpatialAuditRecord:
    step: int
    time: float
    center_value: float
    total_mass: float
    max_value: float
    min_value: float
    diffusion_ratio: float
    transport_ratio: float
    warning: str

def diffusion_ratio(diffusivity: float, dt: float, dx: float) -> float:
    if dx <= 0:
        raise ValueError("dx must be positive")
    if dt <= 0:
        raise ValueError("dt must be positive")
    if diffusivity < 0:
        raise ValueError("diffusivity must be nonnegative")
    return diffusivity * dt / (dx ** 2)

def transport_ratio(velocity: float, dt: float, dx: float) -> float:
    if dx <= 0:
        raise ValueError("dx must be positive")
    if dt <= 0:
        raise ValueError("dt must be positive")
    return velocity * dt / dx

def initialize_field(grid_points: int) -> list[float]:
    if grid_points < 3:
        raise ValueError("grid_points must be at least 3")
    field = [0.0 for _ in range(grid_points)]
    field[grid_points // 2] = 1.0
    return field

def update_advection_diffusion(field: list[float], d_ratio: float, t_ratio: float) -> list[float]:
    updated = field[:]
    for i in range(1, len(field) - 1):
        diffusion_part = d_ratio * (field[i + 1] - 2 * field[i] + field[i - 1])
        transport_part = -t_ratio * (field[i] - field[i - 1])
        updated[i] = field[i] + diffusion_part + transport_part
    updated[0] = 0.0
    updated[-1] = 0.0
    return updated

def simulate_spatial_dynamics(grid_points: int, diffusivity: float, velocity: float, dx: float, dt: float, steps: int) -> list[SpatialAuditRecord]:
    d_ratio = diffusion_ratio(diffusivity, dt, dx)
    t_ratio = transport_ratio(velocity, dt, dx)
    field = initialize_field(grid_points)
    records: list[SpatialAuditRecord] = []
    for step in range(steps + 1):
        records.append(SpatialAuditRecord(
            step=step,
            time=step * dt,
            center_value=field[grid_points // 2],
            total_mass=sum(field) * dx,
            max_value=max(field),
            min_value=min(field),
            diffusion_ratio=d_ratio,
            transport_ratio=t_ratio,
            warning="Spatial dynamics depend on field meaning, boundary conditions, grid spacing, time step, and numerical stability."
        ))
        field = update_advection_diffusion(field, d_ratio, t_ratio)
    return records

def write_outputs(output_dir: Path, records: list[SpatialAuditRecord], summary: dict) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]
    with (output_dir / "tables" / "advection_diffusion_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "advection_diffusion_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    (output_dir / "json" / "advection_diffusion_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    with (output_dir / "tables" / "advection_diffusion_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary.keys()))
        writer.writeheader()
        writer.writerow(summary)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--grid-points", type=int, default=61)
    parser.add_argument("--diffusivity", type=float, default=0.08)
    parser.add_argument("--velocity", type=float, default=0.4)
    parser.add_argument("--dx", type=float, default=1.0)
    parser.add_argument("--dt", type=float, default=0.2)
    parser.add_argument("--steps", type=int, default=120)
    args = parser.parse_args()

    d_ratio = diffusion_ratio(args.diffusivity, args.dt, args.dx)
    t_ratio = transport_ratio(args.velocity, args.dt, args.dx)
    records = simulate_spatial_dynamics(args.grid_points, args.diffusivity, args.velocity, args.dx, args.dt, args.steps)
    summary = {
        "grid_points": args.grid_points,
        "diffusivity": args.diffusivity,
        "velocity": args.velocity,
        "dx": args.dx,
        "dt": args.dt,
        "diffusion_ratio": d_ratio,
        "transport_ratio": t_ratio,
        "final_center_value": records[-1].center_value,
        "interpretation": "The audit records how a localized field moves and spreads under transport and diffusion."
    }
    write_outputs(args.output_dir, records, summary)
    print("Advection-diffusion audit complete.")

if __name__ == "__main__":
    main()
