from __future__ import annotations
import argparse, csv, json
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class GreensTheoremAuditRecord:
    scenario: str
    boundary_segments_per_side: int
    interior_grid_step: float
    boundary_circulation: float
    interior_curl_integral: float
    boundary_flux: float
    interior_divergence_integral: float
    circulation_gap: float
    flux_gap: float
    field_description: str
    region_description: str
    warning: str

def rotation_field(x: float, y: float) -> tuple[float, float]:
    return (-y, x)

def expansion_field(x: float, y: float) -> tuple[float, float]:
    return (x, y)

def planar_curl(x: float, y: float) -> float:
    return 2.0

def planar_divergence(x: float, y: float) -> float:
    return 2.0

def square_boundary_points(segments_per_side: int) -> list[tuple[float, float]]:
    points: list[tuple[float, float]] = []
    for i in range(segments_per_side):
        t = -1.0 + 2.0*i/segments_per_side
        points.append((t, -1.0))
    for i in range(segments_per_side):
        t = -1.0 + 2.0*i/segments_per_side
        points.append((1.0, t))
    for i in range(segments_per_side):
        t = 1.0 - 2.0*i/segments_per_side
        points.append((t, 1.0))
    for i in range(segments_per_side):
        t = 1.0 - 2.0*i/segments_per_side
        points.append((-1.0, t))
    points.append(points[0])
    return points

def boundary_circulation_square(segments_per_side: int) -> float:
    points = square_boundary_points(segments_per_side)
    total = 0.0
    for i in range(len(points)-1):
        x0, y0 = points[i]
        x1, y1 = points[i+1]
        xm, ym = 0.5*(x0+x1), 0.5*(y0+y1)
        dx, dy = x1-x0, y1-y0
        p, q = rotation_field(xm, ym)
        total += p*dx + q*dy
    return total

def boundary_flux_square(segments_per_side: int) -> float:
    points = square_boundary_points(segments_per_side)
    total = 0.0
    for i in range(len(points)-1):
        x0, y0 = points[i]
        x1, y1 = points[i+1]
        xm, ym = 0.5*(x0+x1), 0.5*(y0+y1)
        dx, dy = x1-x0, y1-y0
        # For a positively oriented boundary, outward normal times ds is (dy, -dx).
        nxds, nyds = dy, -dx
        p, q = expansion_field(xm, ym)
        total += p*nxds + q*nyds
    return total

def interior_integral(step: float, value_fn) -> float:
    values = [round(-1.0 + i*step, 10) for i in range(int(2.0/step))]
    total = 0.0
    for x in values:
        for y in values:
            xm, ym = x + 0.5*step, y + 0.5*step
            total += value_fn(xm, ym)*step*step
    return total

def audit_greens_theorem(segments: int, step: float, scenario: str) -> GreensTheoremAuditRecord:
    circulation = boundary_circulation_square(segments)
    curl_integral = interior_integral(step, planar_curl)
    flux = boundary_flux_square(segments)
    divergence_integral = interior_integral(step, planar_divergence)
    warning = (
        "Coarse boundary or interior sampling; refine before interpreting the theorem comparison."
        if segments < 16 or step > 0.25
        else "Synthetic Green's theorem audit; document field, region, orientation, units, and numerical method."
    )
    return GreensTheoremAuditRecord(
        scenario=scenario,
        boundary_segments_per_side=segments,
        interior_grid_step=step,
        boundary_circulation=circulation,
        interior_curl_integral=curl_integral,
        boundary_flux=flux,
        interior_divergence_integral=divergence_integral,
        circulation_gap=abs(circulation-curl_integral),
        flux_gap=abs(flux-divergence_integral),
        field_description="circulation field F=<-y,x>; flux field G=<x,y>; planar curl and divergence equal 2",
        region_description="positively oriented square [-1,1] x [-1,1]",
        warning=warning,
    )

def write_outputs(output_dir: Path, records: list[GreensTheoremAuditRecord]) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]
    with (output_dir / "tables" / "greens_theorem_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "greens_theorem_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    records = [
        audit_greens_theorem(8, 0.5, "coarse_audit"),
        audit_greens_theorem(32, 0.25, "medium_audit"),
        audit_greens_theorem(128, 0.125, "fine_audit"),
    ]
    write_outputs(args.output_dir, records)
    print("Green's theorem audit complete.")

if __name__ == "__main__":
    main()
