from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class SurfaceIntegralAuditRecord:
    scenario: str
    grid_step: float
    patch_count: int
    approximate_surface_area: float
    scalar_surface_integral: float
    vector_flux_integral: float
    average_flux_density: float
    maximum_patch_area: float
    surface_description: str
    warning: str

def height(x: float, y: float) -> float:
    return 0.1 * x * x + 0.05 * y * y

def scalar_field(x: float, y: float, z: float) -> float:
    return 1.0 + 0.2 * z

def vector_field(x: float, y: float, z: float) -> tuple[float, float, float]:
    return (0.1 * x, 0.1 * y, 1.0)

def graph_normal_area_vector(x: float, y: float, dx: float, dy: float) -> tuple[float, float, float]:
    dz_dx = 0.2 * x
    dz_dy = 0.1 * y
    return (-dz_dx * dx * dy, -dz_dy * dx * dy, dx * dy)

def vector_norm(v: tuple[float, float, float]) -> float:
    return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])

def dot(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

def grid_values(step: float) -> list[float]:
    return [round(-1.0 + i * step, 10) for i in range(int(2.0 / step))]

def audit_surface(step: float, scenario: str) -> SurfaceIntegralAuditRecord:
    xs = grid_values(step)
    ys = grid_values(step)

    surface_area = 0.0
    scalar_total = 0.0
    flux_total = 0.0
    patch_areas: list[float] = []
    flux_densities: list[float] = []

    for x in xs:
        for y in ys:
            z = height(x, y)
            area_vector = graph_normal_area_vector(x, y, step, step)
            patch_area = vector_norm(area_vector)
            scalar_value = scalar_field(x, y, z)
            vector_value = vector_field(x, y, z)
            flux = dot(vector_value, area_vector)

            surface_area += patch_area
            scalar_total += scalar_value * patch_area
            flux_total += flux
            patch_areas.append(patch_area)
            flux_densities.append(flux / max(patch_area, 1e-12))

    warning = (
        "Grid step is coarse; curvature and field variation may be undersampled."
        if step > 0.5
        else "Synthetic surface-integral audit; document surface, normal, units, and mesh."
    )

    return SurfaceIntegralAuditRecord(
        scenario=scenario,
        grid_step=step,
        patch_count=len(patch_areas),
        approximate_surface_area=surface_area,
        scalar_surface_integral=scalar_total,
        vector_flux_integral=flux_total,
        average_flux_density=sum(flux_densities) / len(flux_densities),
        maximum_patch_area=max(patch_areas),
        surface_description="graph z = 0.1x^2 + 0.05y^2 over [-1,1] x [-1,1]",
        warning=warning,
    )

def write_outputs(output_dir: Path, records: list[SurfaceIntegralAuditRecord]) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]
    with (output_dir / "tables" / "surface_integral_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "surface_integral_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    records = [
        audit_surface(1.0, "coarse_surface_mesh"),
        audit_surface(0.5, "medium_surface_mesh"),
        audit_surface(0.25, "fine_surface_mesh"),
    ]
    write_outputs(args.output_dir, records)
    print("Surface-integral audit complete.")

if __name__ == "__main__":
    main()
