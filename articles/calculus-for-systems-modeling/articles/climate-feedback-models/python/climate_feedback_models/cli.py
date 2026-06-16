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
    model_type: str
    final_time: float
    final_temperature: float
    interpretation: str

@dataclass(frozen=True)
class SensitivityRecord:
    sensitivity_name: str
    derivative: float
    interpretation: str
    warning: str

def co2_forcing(concentration: float, baseline: float = 280.0) -> float:
    if concentration <= 0 or baseline <= 0:
        raise ValueError("concentration and baseline must be positive")
    return 5.35 * math.log(concentration / baseline)

def one_box_temperature(forcing: float, feedback: float, heat_capacity: float, t: float, t0: float = 0.0) -> float:
    if feedback <= 0 or heat_capacity <= 0:
        raise ValueError("feedback and heat_capacity must be positive under restoring-positive convention")
    equilibrium = forcing / feedback
    return equilibrium + (t0 - equilibrium) * math.exp(-(feedback / heat_capacity) * t)

def simulate_two_box(forcing: float, feedback: float, surface_capacity: float, deep_capacity: float, exchange: float, dt: float, steps: int) -> tuple[float, float]:
    surface = 0.0
    deep = 0.0
    for _ in range(steps):
        d_surface = (forcing - feedback * surface - exchange * (surface - deep)) / surface_capacity
        d_deep = exchange * (surface - deep) / deep_capacity
        surface += dt * d_surface
        deep += dt * d_deep
    return surface, deep

def carbon_feedback_forcing(base_forcing: float, temperature: float, beta_carbon: float) -> float:
    return base_forcing + beta_carbon * temperature

def threshold_feedback(forcing: float, feedback: float, threshold_temp: float, feedback_weakening: float, temperature: float) -> float:
    effective_feedback = feedback - feedback_weakening if temperature >= threshold_temp else feedback
    return forcing / max(effective_feedback, 0.1)

def equilibrium_sensitivity_lambda(forcing: float, feedback: float) -> float:
    return -forcing / (feedback ** 2)

def build_parameter_records() -> list[ParameterRecord]:
    return [
        ParameterRecord("F", 3.7, "W m^-2", "simplified forcing from doubled carbon dioxide", "Forcing depends on forcing agent and scenario."),
        ParameterRecord("lambda", 1.2, "W m^-2 K^-1", "net restoring feedback strength using restoring-positive convention", "Feedback sign convention must be documented."),
        ParameterRecord("C", 8.0, "W yr m^-2 K^-1", "effective surface heat capacity", "Heat capacity summarizes ocean and atmosphere response."),
        ParameterRecord("kappa", 0.7, "W m^-2 K^-1", "surface-to-deep-ocean heat exchange", "Ocean uptake controls transient response."),
        ParameterRecord("Cd", 100.0, "W yr m^-2 K^-1", "deep-ocean heat capacity", "Deep ocean response unfolds over long horizons."),
        ParameterRecord("beta_carbon", 0.15, "W m^-2 K^-1", "simplified carbon-cycle feedback forcing per degree", "Carbon-cycle feedback is process-dependent and uncertain."),
        ParameterRecord("threshold_temp", 2.0, "K", "illustrative nonlinear feedback threshold", "Threshold values require process-specific evidence."),
    ]

def build_scenarios() -> list[ScenarioRecord]:
    forcing = 3.7
    feedback = 1.2
    heat_capacity = 8.0
    one_box_80 = one_box_temperature(forcing, feedback, heat_capacity, 80.0)
    surface, deep = simulate_two_box(forcing, feedback, 8.0, 100.0, 0.7, 0.25, 320)
    adjusted_forcing = carbon_feedback_forcing(forcing, one_box_80, 0.15)
    carbon_feedback_temp = one_box_temperature(adjusted_forcing, feedback, heat_capacity, 80.0)
    weak_feedback = one_box_temperature(forcing, 0.9, heat_capacity, 80.0)
    strong_feedback = one_box_temperature(forcing, 1.6, heat_capacity, 80.0)
    threshold_response = threshold_feedback(forcing, feedback, 2.0, 0.25, one_box_80)
    return [
        ScenarioRecord("one_box_baseline", "one_box_energy_balance", 80.0, one_box_80, "baseline forcing-feedback adjustment"),
        ScenarioRecord("two_box_ocean_uptake", "two_box_energy_balance", 80.0, surface, f"surface warming with deep ocean temperature {deep:.3f}"),
        ScenarioRecord("carbon_cycle_feedback", "carbon_feedback", 80.0, carbon_feedback_temp, "simplified additional forcing from warming-dependent carbon feedback"),
        ScenarioRecord("weak_feedback_high_sensitivity", "feedback_sweep", 80.0, weak_feedback, "weaker restoring feedback produces larger response"),
        ScenarioRecord("strong_feedback_low_sensitivity", "feedback_sweep", 80.0, strong_feedback, "stronger restoring feedback produces smaller response"),
        ScenarioRecord("threshold_feedback_response", "threshold_feedback", 80.0, threshold_response, "illustrative state-dependent weakening of feedback above threshold"),
    ]

def build_sensitivity_records() -> list[SensitivityRecord]:
    return [
        SensitivityRecord(
            "equilibrium_sensitivity_to_lambda",
            equilibrium_sensitivity_lambda(3.7, 1.2),
            "In the simple equilibrium model, temperature response changes strongly as feedback strength changes.",
            "Sensitivity to feedback strength depends on sign convention and simplified model structure."
        )
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
    sensitivities = [asdict(record) for record in build_sensitivity_records()]

    write_csv(output_dir/"tables"/"climate_feedback_parameter_records.csv", parameters)
    write_csv(output_dir/"tables"/"climate_feedback_scenario_records.csv", scenarios)
    write_csv(output_dir/"tables"/"climate_feedback_sensitivity_records.csv", sensitivities)

    audit = {
        "parameter_records": parameters,
        "scenario_records": scenarios,
        "sensitivity_records": sensitivities,
        "sign_convention": "Restoring-positive convention: C dT/dt = F - lambda T.",
        "interpretation_warning": "Climate feedback model outputs depend on forcing assumptions, feedback sign convention, heat uptake, carbon-cycle response, uncertainty, and claim boundaries."
    }
    (output_dir/"json"/"climate_feedback_audit.json").write_text(json.dumps(audit, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Climate Feedback Model Audit", "", "## Scenario Records"]
    for row in scenarios:
        report.append(f"- **{row['scenario_name']}** ({row['model_type']}): final temperature at t={row['final_time']} is {row['final_temperature']:.3f}. {row['interpretation']}.")
    report += ["", "## Sensitivity Records"]
    for row in sensitivities:
        report.append(f"- **{row['sensitivity_name']}**: derivative={row['derivative']:.4f}. {row['warning']}")
    report.append("")
    report.append("Sign convention: restoring-positive convention, C dT/dt = F - lambda T.")
    report.append("Climate feedback model outputs depend on forcing assumptions, feedback sign convention, heat uptake, carbon-cycle response, uncertainty, and claim boundaries.")
    (output_dir/"reports"/"climate_feedback_audit.md").write_text("\n".join(report)+"\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Climate feedback audit outputs generated.")

if __name__ == "__main__":
    main()
