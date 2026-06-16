from __future__ import annotations
import argparse, csv, json
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class FiniteDifferenceRecord:
    step: int
    time: float
    center_value: float
    total_mass: float
    max_value: float
    left_boundary: float
    right_boundary: float
    diffusion_ratio: float
    stability_status: str
    warning: str

def forward_difference(f_i: float, f_ip1: float, dx: float) -> float:
    return (f_ip1 - f_i) / dx

def backward_difference(f_im1: float, f_i: float, dx: float) -> float:
    return (f_i - f_im1) / dx

def central_difference(f_im1: float, f_ip1: float, dx: float) -> float:
    return (f_ip1 - f_im1) / (2.0 * dx)

def second_central_difference(f_im1: float, f_i: float, f_ip1: float, dx: float) -> float:
    return (f_ip1 - 2.0 * f_i + f_im1) / (dx * dx)

def diffusion_ratio(diffusivity: float, dt: float, dx: float) -> float:
    return diffusivity * dt / (dx * dx)

def initialize_field(grid_points: int) -> list[float]:
    field = [0.0 for _ in range(grid_points)]
    field[grid_points // 2] = 1.0
    return field

def update_diffusion(field: list[float], ratio: float) -> list[float]:
    updated = field[:]
    for i in range(1, len(field) - 1):
        updated[i] = field[i] + ratio * (field[i + 1] - 2.0 * field[i] + field[i - 1])
    updated[0] = 0.0
    updated[-1] = 0.0
    return updated

def simulate_finite_difference_diffusion(grid_points: int, diffusivity: float, dx: float, dt: float, steps: int) -> list[FiniteDifferenceRecord]:
    ratio = diffusion_ratio(diffusivity, dt, dx)
    status = "stable_for_basic_explicit_1d_diffusion" if ratio <= 0.5 else "unstable_risk"
    field = initialize_field(grid_points)
    records = []
    for step in range(steps + 1):
        records.append(FiniteDifferenceRecord(
            step=step,
            time=step * dt,
            center_value=field[grid_points // 2],
            total_mass=sum(field) * dx,
            max_value=max(field),
            left_boundary=field[0],
            right_boundary=field[-1],
            diffusion_ratio=ratio,
            stability_status=status,
            warning="Finite difference results depend on grid spacing, time step, stencil, boundary condition, stability, and convergence checks."
        ))
        field = update_diffusion(field, ratio)
    return records

def write_outputs(output_dir: Path, records: list[FiniteDifferenceRecord], summary: dict) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]
    with (output_dir / "tables" / "finite_difference_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "finite_difference_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    (output_dir / "json" / "finite_difference_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--grid-points", type=int, default=61)
    parser.add_argument("--diffusivity", type=float, default=0.08)
    parser.add_argument("--dx", type=float, default=1.0)
    parser.add_argument("--dt", type=float, default=0.2)
    parser.add_argument("--steps", type=int, default=120)
    args = parser.parse_args()

    ratio = diffusion_ratio(args.diffusivity, args.dt, args.dx)
    records = simulate_finite_difference_diffusion(args.grid_points, args.diffusivity, args.dx, args.dt, args.steps)
    summary = {
        "grid_points": args.grid_points,
        "diffusivity": args.diffusivity,
        "dx": args.dx,
        "dt": args.dt,
        "steps": args.steps,
        "diffusion_ratio": ratio,
        "stability_note": "For a basic explicit one-dimensional diffusion scheme, diffusion_ratio <= 0.5 is a common stability condition.",
        "interpretation": "The workflow audits how a local finite difference stencil evolves a synthetic diffusion field."
    }
    write_outputs(args.output_dir, records, summary)
    print("Finite difference audit complete.")

if __name__ == "__main__":
    main()
