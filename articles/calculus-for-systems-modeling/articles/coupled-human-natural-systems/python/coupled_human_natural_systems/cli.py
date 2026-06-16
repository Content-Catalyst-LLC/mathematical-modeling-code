from __future__ import annotations
import argparse, csv, json
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class ParameterRecord:
    parameter_name: str
    value: float
    unit: str
    interpretation: str
    warning: str

@dataclass(frozen=True)
class ScenarioRecord:
    scenario_name: str
    model_type: str
    final_human_pressure: float
    final_natural_stock: float
    cumulative_extraction: float
    cumulative_burden: float
    interpretation: str

@dataclass(frozen=True)
class DiagnosticRecord:
    diagnostic_name: str
    value: float
    unit: str
    interpretation: str
    warning: str

def regeneration(stock: float, growth_rate: float, carrying_capacity: float) -> float:
    return growth_rate * stock * (1 - stock / carrying_capacity)

def extraction(efficiency: float, effort: float, stock: float) -> float:
    return efficiency * effort * stock

def adaptive_effort_step(effort: float, perceived_scarcity: float, governance_strength: float, adjustment_rate: float, dt: float) -> float:
    target_reduction = governance_strength * perceived_scarcity
    return max(0.0, effort - adjustment_rate * target_reduction * dt)

def natural_stock_step(stock: float, growth_rate: float, carrying_capacity: float, extraction_amount: float, stress: float, dt: float) -> float:
    change = regeneration(stock, growth_rate, carrying_capacity) - extraction_amount - stress
    return max(0.0, stock + change * dt)

def distributional_burden(exposure: float, vulnerability: float, adaptation: float) -> float:
    return max(0.0, exposure * vulnerability - adaptation)

def threshold_warning(stock: float, threshold: float) -> str:
    return "below_threshold_review_required" if stock < threshold else "above_threshold_monitoring_required"

def simulate_coupled_system(
    scenario_name: str,
    growth_rate: float,
    carrying_capacity: float,
    efficiency: float,
    initial_effort: float,
    governance_strength: float,
    adjustment_rate: float,
    stress: float,
    initial_stock: float,
    vulnerability: float,
    adaptation: float,
    dt: float,
    steps: int
) -> ScenarioRecord:
    stock = initial_stock
    effort = initial_effort
    cumulative_extraction = 0.0
    cumulative_burden = 0.0
    for _ in range(steps):
        scarcity = max(0.0, 1 - stock / carrying_capacity)
        harvest = extraction(efficiency, effort, stock)
        stock = natural_stock_step(stock, growth_rate, carrying_capacity, harvest, stress, dt)
        effort = adaptive_effort_step(effort, scarcity, governance_strength, adjustment_rate, dt)
        burden = distributional_burden(exposure=scarcity + stress, vulnerability=vulnerability, adaptation=adaptation)
        cumulative_extraction += harvest * dt
        cumulative_burden += burden * dt

    return ScenarioRecord(
        scenario_name=scenario_name,
        model_type="resource_governance_feedback",
        final_human_pressure=effort,
        final_natural_stock=stock,
        cumulative_extraction=cumulative_extraction,
        cumulative_burden=cumulative_burden,
        interpretation="Coupled outcome depends on regeneration, extraction, stress, governance, adaptation, and vulnerability."
    )

def build_parameter_records() -> list[ParameterRecord]:
    return [
        ParameterRecord("r", 0.08, "per year", "natural regeneration rate", "Regeneration may vary with habitat, climate, age structure, and system state."),
        ParameterRecord("K", 100.0, "stock units", "carrying capacity", "Carrying capacity may change with climate, land use, pollution, or habitat loss."),
        ParameterRecord("q_e", 0.003, "per effort per stock", "extraction efficiency", "Technology can increase pressure or reduce waste depending on context."),
        ParameterRecord("A", 12.0, "effort units", "human extraction effort", "Effort reflects livelihoods, demand, technology, and constraints."),
        ParameterRecord("G", 0.60, "index", "governance strength", "Governance quality includes legitimacy, enforcement, resources, and trust."),
        ParameterRecord("mu", 0.20, "per year", "adjustment rate", "Human response may be slow, unequal, or constrained."),
        ParameterRecord("Nc", 30.0, "stock units", "critical natural threshold", "Thresholds are uncertain and should be stress-tested."),
    ]

def build_scenarios() -> list[ScenarioRecord]:
    dt = 0.25
    steps = 160
    return [
        simulate_coupled_system("baseline_coupled_resource", 0.08, 100.0, 0.003, 12.0, 0.60, 0.20, 0.25, 80.0, 1.2, 0.10, dt, steps),
        simulate_coupled_system("high_extraction_low_governance", 0.08, 100.0, 0.004, 18.0, 0.20, 0.10, 0.35, 80.0, 1.6, 0.05, dt, steps),
        simulate_coupled_system("restoration_and_adaptation", 0.10, 110.0, 0.0025, 10.0, 0.85, 0.30, 0.15, 80.0, 1.0, 0.25, dt, steps),
    ]

def build_diagnostics() -> list[DiagnosticRecord]:
    return [
        DiagnosticRecord("baseline_regeneration_at_stock_80", regeneration(80.0, 0.08, 100.0), "stock units per year", "regeneration at stock 80", "Regeneration may vary with habitat, climate, and system state."),
        DiagnosticRecord("baseline_extraction_example", extraction(0.003, 12.0, 80.0), "stock units per year", "effort-based extraction example", "Extraction assumptions should include technology, livelihoods, and constraints."),
        DiagnosticRecord("burden_example", distributional_burden(0.6, 1.4, 0.2), "burden units", "distributional burden example", "Aggregate outcomes can hide unequal burden."),
        DiagnosticRecord("threshold_status_example", 1.0 if threshold_warning(25, 30) == "below_threshold_review_required" else 0.0, "binary", "threshold review status", "Thresholds are uncertain and should be stress-tested."),
    ]

def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

def write_outputs(output_dir: Path) -> None:
    (output_dir/"tables").mkdir(parents=True, exist_ok=True)
    (output_dir/"json").mkdir(parents=True, exist_ok=True)
    (output_dir/"reports").mkdir(parents=True, exist_ok=True)

    parameters = [asdict(record) for record in build_parameter_records()]
    scenarios = [asdict(record) for record in build_scenarios()]
    diagnostics = [asdict(record) for record in build_diagnostics()]

    write_csv(output_dir/"tables"/"coupled_parameter_records.csv", parameters)
    write_csv(output_dir/"tables"/"coupled_scenario_records.csv", scenarios)
    write_csv(output_dir/"tables"/"coupled_diagnostic_records.csv", diagnostics)

    audit = {
        "parameter_records": parameters,
        "scenario_records": scenarios,
        "diagnostics": diagnostics,
        "interpretation_warning": "Coupled human-natural systems outputs depend on boundary definitions, human assumptions, ecological assumptions, feedback mechanisms, governance assumptions, distributional effects, uncertainty, and claim boundaries."
    }
    (output_dir/"json"/"coupled_human_natural_systems_audit.json").write_text(json.dumps(audit, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Coupled Human-Natural Systems Audit", "", "## Scenario Records"]
    for row in scenarios:
        report.append(f"- **{row['scenario_name']}** ({row['model_type']}): final effort={row['final_human_pressure']:.3f}, final natural stock={row['final_natural_stock']:.3f}, cumulative extraction={row['cumulative_extraction']:.3f}, cumulative burden={row['cumulative_burden']:.3f}. {row['interpretation']}")
    report += ["", "## Diagnostic Records"]
    for row in diagnostics:
        report.append(f"- **{row['diagnostic_name']}**: {row['value']:.3f} {row['unit']}. {row['warning']}")
    report.append("")
    report.append("Coupled human-natural systems outputs depend on boundary definitions, human assumptions, ecological assumptions, feedback mechanisms, governance assumptions, distributional effects, uncertainty, and claim boundaries.")
    (output_dir/"reports"/"coupled_human_natural_systems_audit.md").write_text("\n".join(report)+"\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Coupled human-natural systems audit outputs generated.")

if __name__ == "__main__":
    main()
