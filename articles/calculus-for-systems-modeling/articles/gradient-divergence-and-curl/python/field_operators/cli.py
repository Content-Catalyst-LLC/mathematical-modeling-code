from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class FieldOperatorAuditRecord:
    scenario: str
    grid_step: float
    point_count: int
    mean_gradient_magnitude: float
    maximum_gradient_magnitude: float
    mean_divergence: float
    mean_curl: float
    maximum_abs_curl: float
    field_description: str
    warning: str

def scalar_field(x: float, y: float) -> float:
    return x*x + y*y

def vector_field(x: float, y: float) -> tuple[float, float]:
    return (-y, x)

def gradient(x: float, y: float) -> tuple[float, float]:
    return (2.0*x, 2.0*y)

def divergence(x: float, y: float) -> float:
    return 0.0

def curl_2d(x: float, y: float) -> float:
    return 2.0

def grid_values(step: float) -> list[float]:
    return [round(-1.0 + i*step, 10) for i in range(int(2.0/step) + 1)]

def audit_field_operators(step: float, scenario: str) -> FieldOperatorAuditRecord:
    values = grid_values(step)
    grad_magnitudes: list[float] = []
    divergences: list[float] = []
    curls: list[float] = []

    for x in values:
        for y in values:
            gx, gy = gradient(x, y)
            grad_magnitudes.append(math.sqrt(gx*gx + gy*gy))
            divergences.append(divergence(x, y))
            curls.append(curl_2d(x, y))

    warning = (
        "Grid step is coarse; local derivative structure may be undersampled."
        if step > 0.5
        else "Synthetic field-operator audit; document field definitions, units, grid, and boundary rules."
    )

    return FieldOperatorAuditRecord(
        scenario=scenario,
        grid_step=step,
        point_count=len(values)*len(values),
        mean_gradient_magnitude=sum(grad_magnitudes)/len(grad_magnitudes),
        maximum_gradient_magnitude=max(grad_magnitudes),
        mean_divergence=sum(divergences)/len(divergences),
        mean_curl=sum(curls)/len(curls),
        maximum_abs_curl=max(abs(value) for value in curls),
        field_description="scalar f=x^2+y^2; vector F=<-y,x>",
        warning=warning,
    )

def write_outputs(output_dir: Path, records: list[FieldOperatorAuditRecord]) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]
    with (output_dir / "tables" / "field_operator_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "field_operator_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    records = [
        audit_field_operators(1.0, "coarse_grid"),
        audit_field_operators(0.5, "medium_grid"),
        audit_field_operators(0.25, "fine_grid"),
    ]
    write_outputs(args.output_dir, records)
    print("Field-operator audit complete.")

if __name__ == "__main__":
    main()
