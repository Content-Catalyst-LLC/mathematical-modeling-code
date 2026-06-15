from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class ChangeOfVariablesAuditRecord:
    scenario: str
    radius: float
    radial_step: float
    angular_step: float
    polar_total: float
    cartesian_grid_total: float
    absolute_difference: float
    relative_difference: float
    jacobian_rule: str
    warning: str

def exposure_cartesian(x: float, y: float) -> float:
    r = math.sqrt(x * x + y * y)
    return 20.0 * math.exp(-0.4 * r)

def exposure_polar(r: float, theta: float) -> float:
    return 20.0 * math.exp(-0.4 * r)

def polar_total(radius: float, radial_step: float, angular_step: float) -> float:
    total = 0.0
    r = radial_step / 2.0
    while r < radius:
        theta = angular_step / 2.0
        while theta < 2.0 * math.pi:
            total += exposure_polar(r, theta) * r * radial_step * angular_step
            theta += angular_step
        r += radial_step
    return total

def cartesian_grid_total(radius: float, step: float) -> float:
    total = 0.0
    n = int((2.0 * radius) / step)
    for i in range(n + 1):
        x = -radius + i * step
        for j in range(n + 1):
            y = -radius + j * step
            if x * x + y * y <= radius * radius:
                total += exposure_cartesian(x, y) * step * step
    return total

def audit_change_of_variables(radius: float, radial_step: float, angular_step: float, scenario: str) -> ChangeOfVariablesAuditRecord:
    p_total = polar_total(radius, radial_step, angular_step)
    c_total = cartesian_grid_total(radius, radial_step)
    absolute_difference = abs(p_total - c_total)
    relative_difference = absolute_difference / max(abs(p_total), 1e-12)
    warning = (
        "Resolution is coarse; transformed and Cartesian approximations may differ."
        if radial_step > 0.5
        else "Polar Jacobian factor r included; compare domain and resolution assumptions."
    )
    return ChangeOfVariablesAuditRecord(
        scenario=scenario,
        radius=radius,
        radial_step=radial_step,
        angular_step=angular_step,
        polar_total=p_total,
        cartesian_grid_total=c_total,
        absolute_difference=absolute_difference,
        relative_difference=relative_difference,
        jacobian_rule="dA = r dr dtheta",
        warning=warning,
    )

def write_outputs(output_dir: Path, records: list[ChangeOfVariablesAuditRecord]) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(r) for r in records]
    with (output_dir / "tables" / "change_of_variables_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "change_of_variables_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    records = [
        audit_change_of_variables(3.0, 0.5, math.pi / 24.0, "medium_polar_grid"),
        audit_change_of_variables(3.0, 0.25, math.pi / 48.0, "fine_polar_grid"),
        audit_change_of_variables(3.0, 0.125, math.pi / 96.0, "very_fine_polar_grid"),
    ]
    write_outputs(args.output_dir, records)
    print("Change-of-variables audit complete.")

if __name__ == "__main__":
    main()
