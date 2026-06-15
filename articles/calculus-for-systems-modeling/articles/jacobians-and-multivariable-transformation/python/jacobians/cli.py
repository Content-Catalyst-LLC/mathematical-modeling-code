from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

Matrix2 = tuple[tuple[float, float], tuple[float, float]]

@dataclass(frozen=True)
class JacobianAuditRecord:
    x: float
    y: float
    dx: float
    dy: float
    j11: float
    j12: float
    j21: float
    j22: float
    determinant: float
    approximate_change_1: float
    approximate_change_2: float
    actual_change_1: float
    actual_change_2: float
    error_norm: float
    warning: str

def F(x: float, y: float) -> tuple[float, float]:
    return (x * x + y, x * y + 3.0 * y)

def jacobian(x: float, y: float) -> Matrix2:
    return ((2.0 * x, 1.0), (y, x + 3.0))

def determinant_2x2(J: Matrix2) -> float:
    return J[0][0] * J[1][1] - J[0][1] * J[1][0]

def trace_2x2(J: Matrix2) -> float:
    return J[0][0] + J[1][1]

def condition_warning(det: float) -> str:
    if abs(det) <= 1e-8:
        return "Jacobian is singular or near singular."
    if abs(det) < 0.25:
        return "Jacobian determinant is small; local inversion may be fragile."
    return ""

def audit_case(x: float, y: float, dx: float, dy: float) -> JacobianAuditRecord:
    J = jacobian(x, y)
    baseline = F(x, y)
    actual = F(x + dx, y + dy)
    approximate_change = (
        J[0][0] * dx + J[0][1] * dy,
        J[1][0] * dx + J[1][1] * dy,
    )
    actual_change = (actual[0] - baseline[0], actual[1] - baseline[1])
    error_norm = math.sqrt((actual_change[0] - approximate_change[0]) ** 2 + (actual_change[1] - approximate_change[1]) ** 2)
    det = determinant_2x2(J)
    return JacobianAuditRecord(
        x=x, y=y, dx=dx, dy=dy,
        j11=J[0][0], j12=J[0][1], j21=J[1][0], j22=J[1][1],
        determinant=det,
        approximate_change_1=approximate_change[0],
        approximate_change_2=approximate_change[1],
        actual_change_1=actual_change[0],
        actual_change_2=actual_change[1],
        error_norm=error_norm,
        warning=condition_warning(det),
    )

def write_outputs(output_dir: Path, records: list[JacobianAuditRecord]) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(r) for r in records]
    with (output_dir / "tables" / "jacobian_transformation_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "jacobian_transformation_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    records = [
        audit_case(2.0, 1.0, 0.1, -0.05),
        audit_case(2.0, 1.0, 0.5, 0.5),
        audit_case(0.0, 0.0, 0.1, 0.1),
    ]
    write_outputs(args.output_dir, records)
    print("Jacobian transformation audit complete.")

if __name__ == "__main__":
    main()
