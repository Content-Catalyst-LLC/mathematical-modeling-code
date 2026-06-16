from __future__ import annotations
import argparse, csv, json
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class ContinuityAssumptionRecord:
    assumption_name: str
    model_element: str
    assumption_description: str
    review_question: str
    warning: str

@dataclass(frozen=True)
class MisleadingContinuityRisk:
    risk_name: str
    risk_pattern: str
    possible_consequence: str
    governance_response: str
    status: str

@dataclass(frozen=True)
class SolverDiagnosticRecord:
    diagnostic_name: str
    diagnostic_role: str
    required_record: str
    warning: str

def build_continuity_assumptions() -> list[ContinuityAssumptionRecord]:
    return [
        ContinuityAssumptionRecord("smooth_state_change", "state trajectory x(t)", "state changes gradually over modeled time", "Are shocks, events, or thresholds possible?", "Smooth output does not prove smooth system behavior."),
        ContinuityAssumptionRecord("continuous_rate_function", "dx/dt = f(x,t,theta)", "rate can be represented as a continuous function", "Does the process change through discrete decisions or regime switches?", "Rate continuity should be justified at the modeled scale."),
        ContinuityAssumptionRecord("aggregate_representative_variable", "mean state or average exposure", "aggregate variable represents the system adequately", "Does heterogeneity matter for the claim?", "Averages can hide local stress, inequality, or bottlenecks."),
    ]

def build_risk_records() -> list[MisleadingContinuityRisk]:
    return [
        MisleadingContinuityRisk("false_smoothness", "smooth curve hides structural breaks", "threshold, failure, or event dynamics are missed", "test for breaks and document discontinuities", "review"),
        MisleadingContinuityRisk("equilibrium_bias", "steady-state result is overinterpreted", "transition cost, overshoot, delay, or distributional effect is hidden", "analyze trajectories and stability, not only equilibria", "review"),
        MisleadingContinuityRisk("solver_confidence", "successful computation is mistaken for validation", "numerical artifacts appear as model insight", "record solver method, tolerance, convergence, and warnings", "review"),
        MisleadingContinuityRisk("aggregation_risk", "average hides heterogeneity", "local stress, inequality, or bottlenecks are hidden", "inspect distributions and subgroups", "review"),
        MisleadingContinuityRisk("domain_drift", "local model is extrapolated beyond its domain", "smooth projection exceeds evidence", "define scope and update triggers", "review"),
    ]

def build_solver_diagnostics() -> list[SolverDiagnosticRecord]:
    return [
        SolverDiagnosticRecord("step_size_check", "tests whether results change under smaller time steps", "time step, method, output difference", "Large time steps can miss fast dynamics or threshold crossing."),
        SolverDiagnosticRecord("stiffness_check", "flags fast and slow dynamics that challenge numerical methods", "solver type, stiffness warning, rejected steps", "Stiff systems require solver-specific diagnostics."),
        SolverDiagnosticRecord("convergence_check", "records whether numerical solution converged", "convergence flag, tolerance, iteration count", "A plotted output can hide convergence failure."),
    ]

def write_csv(path: Path, records: list) -> None:
    rows = [asdict(record) for record in records]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)

    assumptions = build_continuity_assumptions()
    risks = build_risk_records()
    diagnostics = build_solver_diagnostics()

    write_csv(output_dir / "tables" / "continuity_assumption_records.csv", assumptions)
    write_csv(output_dir / "tables" / "misleading_continuity_risks.csv", risks)
    write_csv(output_dir / "tables" / "solver_diagnostic_records.csv", diagnostics)

    audit = {
        "continuity_assumptions": [asdict(record) for record in assumptions],
        "misleading_continuity_risks": [asdict(record) for record in risks],
        "solver_diagnostics": [asdict(record) for record in diagnostics],
        "interpretation_warning": "Continuous models are approximations whose smooth assumptions, solver settings, and claim boundaries must be reviewed.",
    }
    (output_dir / "json" / "continuous_model_risk_audit.json").write_text(json.dumps(audit, indent=2, sort_keys=True), encoding="utf-8")

    report_lines = ["# Continuous Model Risk Audit", "", "## Continuity Assumptions"]
    for record in assumptions:
        report_lines.append(f"- **{record.assumption_name}** ({record.model_element}): {record.assumption_description}. Review: {record.review_question}. {record.warning}")
    report_lines.extend(["", "## Misleading Continuity Risks"])
    for record in risks:
        report_lines.append(f"- **{record.risk_name}**: {record.risk_pattern}. Consequence: {record.possible_consequence}. Response: {record.governance_response}.")
    report_lines.extend(["", "## Solver Diagnostics"])
    for record in diagnostics:
        report_lines.append(f"- **{record.diagnostic_name}**: {record.diagnostic_role}. Required record: {record.required_record}. {record.warning}")
    report_lines.extend(["", "Continuous models are approximations whose smooth assumptions, solver settings, and claim boundaries must be reviewed."])

    (output_dir / "reports" / "continuous_model_risk_audit.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Continuous model risk audit outputs generated.")

if __name__ == "__main__":
    main()
