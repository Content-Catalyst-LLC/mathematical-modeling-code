from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class ConstraintAuditRecord:
    x: float
    y: float
    objective_value: float
    constraint_value: float
    constraint_target: float
    constraint_residual: float
    lambda_value: float
    gradient_f_x: float
    gradient_f_y: float
    gradient_g_x: float
    gradient_g_y: float
    stationarity_residual_norm: float
    feasible: bool
    warning: str

def objective(x: float, y: float) -> float:
    return x * x + 2.0 * y * y

def constraint(x: float, y: float) -> float:
    return x + y

def grad_objective(x: float, y: float) -> tuple[float, float]:
    return (2.0 * x, 4.0 * y)

def grad_constraint(x: float, y: float) -> tuple[float, float]:
    return (1.0, 1.0)

def solve_budget_constraint(target: float) -> tuple[float, float, float]:
    # Minimize x^2 + 2y^2 subject to x + y = target.
    y = target / 3.0
    x = 2.0 * target / 3.0
    lambda_value = 2.0 * x
    return x, y, lambda_value

def audit_solution(target: float) -> ConstraintAuditRecord:
    x, y, lambda_value = solve_budget_constraint(target)
    gf = grad_objective(x, y)
    gg = grad_constraint(x, y)
    stationarity = (gf[0] - lambda_value * gg[0], gf[1] - lambda_value * gg[1])
    residual_norm = math.sqrt(stationarity[0] ** 2 + stationarity[1] ** 2)
    constraint_value = constraint(x, y)
    constraint_residual = constraint_value - target
    feasible = abs(constraint_residual) <= 1e-9
    if not feasible:
        warning = "Candidate solution violates the constraint."
    elif residual_norm > 1e-8:
        warning = "Stationarity residual is large."
    else:
        warning = "Multiplier interpretation is local and unit-dependent."
    return ConstraintAuditRecord(
        x=x, y=y, objective_value=objective(x, y),
        constraint_value=constraint_value, constraint_target=target,
        constraint_residual=constraint_residual, lambda_value=lambda_value,
        gradient_f_x=gf[0], gradient_f_y=gf[1],
        gradient_g_x=gg[0], gradient_g_y=gg[1],
        stationarity_residual_norm=residual_norm,
        feasible=feasible, warning=warning,
    )

def write_outputs(output_dir: Path, records: list[ConstraintAuditRecord]) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(r) for r in records]
    with (output_dir / "tables" / "constrained_optimization_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "constrained_optimization_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--targets", type=float, nargs="*", default=[12.0, 18.0, 24.0])
    args = parser.parse_args()
    records = [audit_solution(target) for target in args.targets]
    write_outputs(args.output_dir, records)
    print("Constrained optimization audit complete.")

if __name__ == "__main__":
    main()
