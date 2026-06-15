from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

Matrix2 = tuple[tuple[float, float], tuple[float, float]]

@dataclass(frozen=True)
class HessianAuditRecord:
    x: float
    y: float
    dx: float
    dy: float
    gradient_x: float
    gradient_y: float
    h11: float
    h12: float
    h21: float
    h22: float
    determinant: float
    trace: float
    classification: str
    first_order_change: float
    second_order_change: float
    actual_change: float
    first_order_error: float
    second_order_error: float
    warning: str

def f(x: float, y: float) -> float:
    return x * x + x * y + 3.0 * y * y + 0.2 * x * x * y

def gradient(x: float, y: float) -> tuple[float, float]:
    return (2.0 * x + y + 0.4 * x * y, x + 6.0 * y + 0.2 * x * x)

def hessian(x: float, y: float) -> Matrix2:
    return ((2.0 + 0.4 * y, 1.0 + 0.4 * x), (1.0 + 0.4 * x, 6.0))

def det2(H: Matrix2) -> float:
    return H[0][0] * H[1][1] - H[0][1] * H[1][0]

def trace2(H: Matrix2) -> float:
    return H[0][0] + H[1][1]

def classify_hessian(H: Matrix2) -> str:
    determinant = det2(H)
    h11 = H[0][0]
    if determinant > 0 and h11 > 0:
        return "positive definite"
    if determinant > 0 and h11 < 0:
        return "negative definite"
    if determinant < 0:
        return "indefinite"
    return "semidefinite or inconclusive"

def quadratic_term(H: Matrix2, dx: float, dy: float) -> float:
    return 0.5 * (H[0][0] * dx * dx + 2.0 * H[0][1] * dx * dy + H[1][1] * dy * dy)

def audit_case(x: float, y: float, dx: float, dy: float) -> HessianAuditRecord:
    g = gradient(x, y)
    H = hessian(x, y)
    baseline = f(x, y)
    actual_change = f(x + dx, y + dy) - baseline
    first_order = g[0] * dx + g[1] * dy
    second_order = first_order + quadratic_term(H, dx, dy)
    determinant = det2(H)
    classification = classify_hessian(H)
    warning = ""
    if classification == "indefinite":
        warning = "Hessian is indefinite; local structure is saddle-like."
    elif abs(determinant) < 1e-8:
        warning = "Hessian is singular or nearly singular."
    return HessianAuditRecord(
        x=x, y=y, dx=dx, dy=dy,
        gradient_x=g[0], gradient_y=g[1],
        h11=H[0][0], h12=H[0][1], h21=H[1][0], h22=H[1][1],
        determinant=determinant,
        trace=trace2(H),
        classification=classification,
        first_order_change=first_order,
        second_order_change=second_order,
        actual_change=actual_change,
        first_order_error=abs(actual_change - first_order),
        second_order_error=abs(actual_change - second_order),
        warning=warning,
    )

def write_outputs(output_dir: Path, records: list[HessianAuditRecord]) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(r) for r in records]
    with (output_dir / "tables" / "hessian_curvature_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "hessian_curvature_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    records = [
        audit_case(2.0, 1.0, 0.1, -0.05),
        audit_case(2.0, 1.0, 0.5, 0.5),
        audit_case(-5.0, 0.0, 0.2, 0.1),
    ]
    write_outputs(args.output_dir, records)
    print("Hessian curvature audit complete.")

if __name__ == "__main__":
    main()
