from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class PopulationParameterRecord:
    parameter_name: str
    value: float
    unit: str
    source_status: str
    interpretation: str
    warning: str

@dataclass(frozen=True)
class PopulationScenarioRecord:
    scenario_name: str
    model_type: str
    initial_population: float
    growth_rate: float
    carrying_capacity: float | None
    final_time: float
    final_population: float
    interpretation: str

def exponential_population(n0: float, r: float, t: float) -> float:
    return n0 * math.exp(r * t)

def logistic_population(n0: float, r: float, k: float, t: float) -> float:
    if n0 <= 0:
        raise ValueError("Initial population must be positive.")
    if k <= 0:
        raise ValueError("Carrying capacity must be positive.")
    return k / (1.0 + ((k - n0) / n0) * math.exp(-r * t))

def per_capita_growth(total_growth: float, population: float) -> float:
    if population <= 0:
        raise ValueError("Population must be positive.")
    return total_growth / population

def build_parameter_records() -> list[PopulationParameterRecord]:
    return [
        PopulationParameterRecord("N0", 100.0, "individuals", "synthetic teaching value", "initial population", "Initial values should be measured or estimated with uncertainty in empirical use."),
        PopulationParameterRecord("r", 0.08, "per year", "synthetic teaching value", "intrinsic growth rate", "Growth rates may vary over time and across conditions."),
        PopulationParameterRecord("K", 1000.0, "individuals", "synthetic teaching value", "carrying capacity", "Carrying capacity is assumption-bearing and may change over time."),
    ]

def build_scenarios() -> list[PopulationScenarioRecord]:
    n0, r, k, t = 100.0, 0.08, 1000.0, 40.0
    return [
        PopulationScenarioRecord("exponential_baseline", "exponential", n0, r, None, t, exponential_population(n0, r, t), "unconstrained growth baseline"),
        PopulationScenarioRecord("logistic_capacity_limited", "logistic", n0, r, k, t, logistic_population(n0, r, k, t), "growth limited by carrying capacity"),
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

    parameters = build_parameter_records()
    scenarios = build_scenarios()

    write_csv(output_dir / "tables" / "population_parameter_records.csv", parameters)
    write_csv(output_dir / "tables" / "population_scenario_records.csv", scenarios)

    audit = {
        "parameter_records": [asdict(record) for record in parameters],
        "scenario_records": [asdict(record) for record in scenarios],
        "interpretation_warning": "Population model outputs depend on growth-law assumptions, parameter evidence, scope, and omitted mechanisms.",
    }
    (output_dir / "json" / "population_dynamics_audit.json").write_text(json.dumps(audit, indent=2, sort_keys=True), encoding="utf-8")

    report_lines = ["# Population Dynamics Model Audit", "", "## Parameter Records"]
    for record in parameters:
        report_lines.append(f"- **{record.parameter_name}** = {record.value} {record.unit}. Source: {record.source_status}. {record.warning}")
    report_lines.extend(["", "## Scenario Records"])
    for record in scenarios:
        report_lines.append(f"- **{record.scenario_name}** ({record.model_type}): final population at t={record.final_time} is {record.final_population:.2f}. Interpretation: {record.interpretation}.")
    report_lines.extend(["", "Population model outputs depend on growth-law assumptions, parameter evidence, scope, and omitted mechanisms."])
    (output_dir / "reports" / "population_dynamics_audit.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Population dynamics audit outputs generated.")

if __name__ == "__main__":
    main()
