from __future__ import annotations
import argparse, csv, json
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class SymbolicInspectionRecord:
    item: str
    expression: str
    interpretation: str
    warning: str

def fallback_records() -> list[SymbolicInspectionRecord]:
    return [
        SymbolicInspectionRecord("rate_expression", "r*x*(1 - x/K)", "Logistic growth rate with state x, growth rate r, and carrying capacity K.", "Assumes x, r, and K are positive and K is nonzero."),
        SymbolicInspectionRecord("first_derivative", "r - 2*r*x/K", "Marginal growth effect declines as x increases.", "Derivative interpretation depends on the stated domain."),
        SymbolicInspectionRecord("second_derivative", "-2*r/K", "Curvature is negative for positive r and K.", "Curvature describes the rate expression, not empirical validity."),
        SymbolicInspectionRecord("equilibria", "[0, K]", "Equilibria occur where the rate of change is zero.", "Equilibrium relevance depends on domain and model assumptions."),
        SymbolicInspectionRecord("limit_at_capacity", "0", "Growth rate approaches zero as x approaches carrying capacity.", "Boundary behavior should be checked against the modeled system."),
        SymbolicInspectionRecord("jacobian", "Matrix([[r - 2*r*x/K]])", "One-state Jacobian records the local derivative of the rate function.", "Local linear inspection does not replace nonlinear simulation."),
    ]

def sympy_records() -> list[SymbolicInspectionRecord]:
    try:
        import sympy as sp
    except Exception:
        return fallback_records()

    x, r, K = sp.symbols("x r K", positive=True)
    rate_expression = r * x * (1 - x / K)
    first_derivative = sp.diff(rate_expression, x)
    second_derivative = sp.diff(rate_expression, x, 2)
    equilibria = sp.solve(sp.Eq(rate_expression, 0), x)
    limit_at_capacity = sp.limit(rate_expression, x, K)
    jacobian_one_state = sp.Matrix([rate_expression]).jacobian([x])
    integral_record = sp.integrate(rate_expression, x)

    return [
        SymbolicInspectionRecord("rate_expression", str(rate_expression), "Logistic growth rate with state x, growth rate r, and carrying capacity K.", "Assumes x, r, and K are positive and K is nonzero."),
        SymbolicInspectionRecord("first_derivative", str(first_derivative), "Marginal growth effect declines as x increases.", "Derivative interpretation depends on the stated domain."),
        SymbolicInspectionRecord("second_derivative", str(second_derivative), "Curvature is negative for positive r and K.", "Curvature describes the rate expression, not empirical validity."),
        SymbolicInspectionRecord("integral_record", str(integral_record), "Symbolic antiderivative records accumulated rate structure with respect to x.", "Integral constants, units, and interpretation must be documented."),
        SymbolicInspectionRecord("equilibria", str(equilibria), "Equilibria occur where the rate of change is zero.", "Equilibrium relevance depends on domain and model assumptions."),
        SymbolicInspectionRecord("limit_at_capacity", str(limit_at_capacity), "Growth rate approaches zero as x approaches carrying capacity.", "Boundary behavior should be checked against the modeled system."),
        SymbolicInspectionRecord("jacobian", str(jacobian_one_state), "One-state Jacobian records the local derivative of the rate function.", "Local linear inspection does not replace nonlinear simulation."),
    ]

def write_outputs(output_dir: Path, records: list[SymbolicInspectionRecord]) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]

    with (output_dir / "tables" / "symbolic_model_inspection.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "symbolic_model_inspection.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report_lines = ["# Symbolic Model Inspection\n"]
    for record in records:
        report_lines.append(f"- **{record.item}**: `{record.expression}` — {record.interpretation} Warning: {record.warning}")
    (output_dir / "reports" / "symbolic_model_inspection.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

def domain_warning(expression: str) -> str:
    if "/K" in expression or "K" in expression:
        return "Document K as nonzero and review positivity/domain assumptions."
    return "Document domain assumptions before interpretation."

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    records = sympy_records()
    write_outputs(args.output_dir, records)
    print("Symbolic model inspection outputs generated.")

if __name__ == "__main__":
    main()
