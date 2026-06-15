from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class FieldAuditRecord:
    scenario: str
    grid_step: float
    point_count: int
    scalar_average: float
    scalar_minimum: float
    scalar_maximum: float
    vector_magnitude_average: float
    vector_magnitude_maximum: float
    domain_description: str
    warning: str

def scalar_field(x: float, y: float) -> float:
    return 20.0 + 2.0 * math.sin(x) + 0.5 * y * y

def vector_field(x: float, y: float) -> tuple[float, float]:
    return (-y, x)

def vector_magnitude(vx: float, vy: float) -> float:
    return math.sqrt(vx * vx + vy * vy)

def grid_values(step: float) -> list[float]:
    return [round(-3.0 + i * step, 10) for i in range(int(6.0 / step) + 1)]

def audit_field(step: float, scenario: str) -> FieldAuditRecord:
    scalars: list[float] = []
    magnitudes: list[float] = []
    for x in grid_values(step):
        for y in grid_values(step):
            scalars.append(scalar_field(x, y))
            vx, vy = vector_field(x, y)
            magnitudes.append(vector_magnitude(vx, vy))

    warning = (
        "Grid resolution is coarse; field structure may be undersampled."
        if step > 0.75
        else "Synthetic field audit; document domain, units, and interpolation assumptions."
    )

    return FieldAuditRecord(
        scenario=scenario,
        grid_step=step,
        point_count=len(scalars),
        scalar_average=sum(scalars) / len(scalars),
        scalar_minimum=min(scalars),
        scalar_maximum=max(scalars),
        vector_magnitude_average=sum(magnitudes) / len(magnitudes),
        vector_magnitude_maximum=max(magnitudes),
        domain_description="square domain [-3,3] x [-3,3]",
        warning=warning,
    )

def write_outputs(output_dir: Path, records: list[FieldAuditRecord]) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]
    with (output_dir / "tables" / "field_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "field_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    records = [
        audit_field(1.0, "coarse_grid"),
        audit_field(0.5, "medium_grid"),
        audit_field(0.25, "fine_grid"),
    ]
    write_outputs(args.output_dir, records)
    print("Field audit complete.")

if __name__ == "__main__":
    main()
