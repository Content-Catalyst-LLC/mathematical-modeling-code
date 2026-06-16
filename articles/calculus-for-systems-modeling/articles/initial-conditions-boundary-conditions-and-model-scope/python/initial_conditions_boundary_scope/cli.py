from __future__ import annotations
import argparse, csv, json
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class InitialConditionRecord:
    variable_name: str
    value: float
    unit: str
    source_note: str
    uncertainty_note: str

@dataclass(frozen=True)
class BoundaryConditionRecord:
    boundary_name: str
    boundary_type: str
    value_note: str
    systems_interpretation: str
    warning: str

@dataclass(frozen=True)
class ScopeRecord:
    scope_dimension: str
    allowed_domain: str
    intended_use: str
    review_warning: str

def build_initial_conditions() -> list[InitialConditionRecord]:
    return [
        InitialConditionRecord("population_stock", 10.0, "state units", "synthetic teaching baseline", "baseline chosen for demonstration"),
        InitialConditionRecord("time_start", 0.0, "time units", "model convention", "no empirical timestamp attached"),
    ]

def build_boundary_conditions() -> list[BoundaryConditionRecord]:
    return [
        BoundaryConditionRecord("left_edge", "no_flux", "zero normal flux", "material does not leave through the left boundary", "No-flux boundaries may overstate retention if the real system is open."),
        BoundaryConditionRecord("right_edge", "absorbing", "outflow allowed", "material can leave the modeled domain", "Absorbing boundaries may understate feedback from surroundings."),
    ]

def build_scope_records() -> list[ScopeRecord]:
    return [
        ScopeRecord("temporal_scope", "0 to 20 time units", "short-horizon teaching simulation", "Do not interpret as long-term forecast."),
        ScopeRecord("parameter_scope", "growth_rate between 0.1 and 0.6", "local sensitivity and teaching examples", "Do not use outside tested parameter range without review."),
        ScopeRecord("decision_scope", "exploratory and educational use", "model interpretation and workflow demonstration", "Do not treat as direct decision prescription."),
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

    initial_conditions = build_initial_conditions()
    boundary_conditions = build_boundary_conditions()
    scope_records = build_scope_records()

    write_csv(output_dir / "tables" / "initial_conditions.csv", initial_conditions)
    write_csv(output_dir / "tables" / "boundary_conditions.csv", boundary_conditions)
    write_csv(output_dir / "tables" / "scope_records.csv", scope_records)

    audit = {
        "initial_conditions": [asdict(record) for record in initial_conditions],
        "boundary_conditions": [asdict(record) for record in boundary_conditions],
        "scope_records": [asdict(record) for record in scope_records],
    }
    (output_dir / "json" / "condition_scope_audit.json").write_text(json.dumps(audit, indent=2, sort_keys=True), encoding="utf-8")

    report_lines = ["# Condition and Scope Audit", "", "## Initial Conditions"]
    for record in initial_conditions:
        report_lines.append(f"- **{record.variable_name}** = {record.value} {record.unit}; source: {record.source_note}; uncertainty: {record.uncertainty_note}")
    report_lines.extend(["", "## Boundary Conditions"])
    for record in boundary_conditions:
        report_lines.append(f"- **{record.boundary_name}** ({record.boundary_type}): {record.systems_interpretation}. {record.warning}")
    report_lines.extend(["", "## Scope Records"])
    for record in scope_records:
        report_lines.append(f"- **{record.scope_dimension}**: {record.allowed_domain}. {record.review_warning}")

    (output_dir / "reports" / "condition_scope_audit.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Condition and scope audit outputs generated.")

if __name__ == "__main__":
    main()
