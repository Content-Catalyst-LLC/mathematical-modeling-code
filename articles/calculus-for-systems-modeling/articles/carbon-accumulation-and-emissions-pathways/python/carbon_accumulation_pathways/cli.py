from __future__ import annotations
import argparse, csv, json, math
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
    pathway_type: str
    final_year: int
    cumulative_emissions: float
    atmospheric_burden: float
    budget_exhaustion_year: int | None
    interpretation: str

@dataclass(frozen=True)
class BudgetRecord:
    scenario_name: str
    cumulative_emissions: float
    budget: float
    exceeds_budget: bool
    overshoot_amount: float
    warning: str

def linear_decline_emissions(e0: float, years: int) -> list[float]:
    return [max(0.0, e0 * (1 - year / years)) for year in range(years + 1)]

def exponential_decline_emissions(e0: float, rate: float, years: int) -> list[float]:
    return [e0 * math.exp(-rate * year) for year in range(years + 1)]

def constant_emissions(e0: float, years: int) -> list[float]:
    return [e0 for _ in range(years + 1)]

def overshoot_pathway(e0: float, decline_years: int, negative_years: int, removal_rate: float) -> list[float]:
    positive = linear_decline_emissions(e0, decline_years)
    negative = [-removal_rate for _ in range(negative_years)]
    return positive + negative

def net_zero_plateau(e0: float, plateau_years: int, decline_years: int) -> list[float]:
    return [e0 for _ in range(plateau_years)] + linear_decline_emissions(e0, decline_years)

def cumulative_sum(pathway: list[float]) -> float:
    return sum(pathway)

def atmospheric_burden_fixed_airborne(pathway: list[float], airborne_fraction: float) -> float:
    return airborne_fraction * cumulative_sum(pathway)

def atmospheric_burden_impulse(pathway: list[float], persistent: float = 0.2) -> float:
    coefficients = [(0.3, 4.0), (0.25, 35.0), (0.25, 200.0)]
    burden = 0.0
    horizon = len(pathway)
    for emission_year, emission in enumerate(pathway):
        age = horizon - 1 - emission_year
        response = persistent + sum(weight * math.exp(-age / tau) for weight, tau in coefficients)
        burden += emission * response
    return burden

def carbon_budget_exhaustion_year(pathway: list[float], budget: float) -> int | None:
    total = 0.0
    for year, emission in enumerate(pathway):
        total += emission
        if total >= budget:
            return year
    return None

def sink_feedback_adjusted_burden(pathway: list[float], airborne_fraction: float, temperature_proxy: float, sink_feedback_strength: float) -> float:
    adjusted_af = min(0.95, max(0.0, airborne_fraction + sink_feedback_strength * temperature_proxy))
    return atmospheric_burden_fixed_airborne(pathway, adjusted_af)

def build_parameter_records() -> list[ParameterRecord]:
    return [
        ParameterRecord("E0", 40.0, "GtCO2 per year", "initial annual emissions", "Accounting boundary must be documented."),
        ParameterRecord("decline_rate", 0.08, "per year", "exponential emissions decline rate", "Pathway assumptions should not be presented as predictions."),
        ParameterRecord("airborne_fraction", 0.45, "fraction", "fixed simplified airborne fraction", "Airborne fraction is not constant across all time scales and scenarios."),
        ParameterRecord("budget", 500.0, "GtCO2", "illustrative remaining carbon budget", "Carbon budgets depend on temperature goal, probability framing, and uncertainty."),
        ParameterRecord("removal_rate", 5.0, "GtCO2 per year", "illustrative negative-emissions rate", "Removal feasibility, permanence, scale, and governance must be reviewed."),
        ParameterRecord("persistent_fraction", 0.2, "fraction", "persistent long-lived carbon response component", "Impulse response assumptions shape long-term burden."),
        ParameterRecord("sink_feedback_strength", 0.05, "fraction per K", "illustrative warming-related sink weakening", "Carbon-cycle feedback is process-dependent and uncertain."),
    ]

def build_pathways() -> list[tuple[str, str, list[float], str]]:
    return [
        ("constant_emissions", "constant", constant_emissions(40.0, 30), "constant emissions continue accumulating carbon"),
        ("linear_decline_to_zero", "linear_decline", linear_decline_emissions(40.0, 30), "linear decline reaches zero after 30 years"),
        ("exponential_decline", "exponential_decline", exponential_decline_emissions(40.0, 0.08, 30), "exponential decline reduces early cumulative burden"),
        ("net_zero_after_plateau", "net_zero", net_zero_plateau(40.0, 10, 25), "delayed action increases cumulative burden before net zero"),
        ("overshoot_with_negative_emissions", "overshoot", overshoot_pathway(40.0, 30, 20, 5.0), "negative emissions partly offset earlier cumulative emissions"),
    ]

def build_scenarios(budget: float = 500.0) -> list[ScenarioRecord]:
    records = []
    for name, pathway_type, pathway, note in build_pathways():
        records.append(
            ScenarioRecord(
                name,
                pathway_type,
                len(pathway) - 1,
                cumulative_sum(pathway),
                atmospheric_burden_impulse(pathway),
                carbon_budget_exhaustion_year(pathway, budget),
                note
            )
        )
    return records

def build_budget_records(budget: float = 500.0) -> list[BudgetRecord]:
    records = []
    for record in build_scenarios(budget):
        overshoot = max(0.0, record.cumulative_emissions - budget)
        records.append(
            BudgetRecord(
                record.scenario_name,
                record.cumulative_emissions,
                budget,
                record.cumulative_emissions > budget,
                overshoot,
                "Carbon budgets are conditional estimates, not exact guarantees."
            )
        )
    return records

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
    budgets = [asdict(record) for record in build_budget_records()]

    write_csv(output_dir/"tables"/"carbon_pathway_parameter_records.csv", parameters)
    write_csv(output_dir/"tables"/"carbon_pathway_scenario_records.csv", scenarios)
    write_csv(output_dir/"tables"/"carbon_budget_records.csv", budgets)

    audit = {
        "parameter_records": parameters,
        "scenario_records": scenarios,
        "budget_records": budgets,
        "interpretation_warning": "Carbon pathway outputs depend on accounting boundaries, emissions pathway assumptions, sink behavior, persistence, removals, carbon-budget framing, and claim boundaries."
    }
    (output_dir/"json"/"carbon_accumulation_audit.json").write_text(json.dumps(audit, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Carbon Accumulation and Emissions Pathway Audit", "", "## Scenario Records"]
    for row in scenarios:
        report.append(f"- **{row['scenario_name']}** ({row['pathway_type']}): cumulative emissions={row['cumulative_emissions']:.2f}, atmospheric burden={row['atmospheric_burden']:.2f}. {row['interpretation']}.")
    report += ["", "## Budget Records"]
    for row in budgets:
        status = "exceeds budget" if row["exceeds_budget"] else "within budget"
        report.append(f"- **{row['scenario_name']}**: {status}; overshoot={row['overshoot_amount']:.2f}. {row['warning']}")
    report.append("")
    report.append("Carbon pathway outputs depend on accounting boundaries, emissions pathway assumptions, sink behavior, persistence, removals, carbon-budget framing, and claim boundaries.")
    (output_dir/"reports"/"carbon_accumulation_audit.md").write_text("\n".join(report)+"\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Carbon accumulation audit outputs generated.")

if __name__ == "__main__":
    main()
