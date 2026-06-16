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
    final_time: float
    final_temperature: float
    equilibrium_temperature: float
    adjustment_time: float
    interpretation: str

@dataclass(frozen=True)
class DiagnosticRecord:
    diagnostic_name: str
    value: float
    unit: str
    interpretation: str
    warning: str

def equilibrium_temperature(forcing: float, feedback: float) -> float:
    if feedback <= 0:
        raise ValueError("feedback must be positive")
    return forcing / feedback

def adjustment_time(heat_capacity: float, feedback: float) -> float:
    if feedback <= 0:
        raise ValueError("feedback must be positive")
    return heat_capacity / feedback

def one_layer_response(forcing: float, feedback: float, heat_capacity: float, initial_temperature: float, dt: float, steps: int) -> float:
    temperature = initial_temperature
    for _ in range(steps):
        imbalance = forcing - feedback * temperature
        temperature += (imbalance / heat_capacity) * dt
    return temperature

def two_layer_response(forcing: float, feedback: float, exchange: float, c_upper: float, c_deep: float, t_upper0: float, t_deep0: float, dt: float, steps: int) -> tuple[float, float]:
    t_upper = t_upper0
    t_deep = t_deep0
    for _ in range(steps):
        exchange_flux = exchange * (t_upper - t_deep)
        t_upper += ((forcing - feedback * t_upper - exchange_flux) / c_upper) * dt
        t_deep += (exchange_flux / c_deep) * dt
    return t_upper, t_deep

def absorbed_solar(solar_constant: float, albedo: float) -> float:
    return solar_constant * (1 - albedo) / 4

def linear_outgoing_radiation(a: float, b: float, temperature: float) -> float:
    return a + b * temperature

def surface_energy_partition(net_radiation: float, sensible: float, latent: float, ground: float) -> float:
    return net_radiation - sensible - latent - ground

def building_temperature_step(temperature: float, heat_capacity: float, q_heat: float, q_solar: float, q_internal: float, q_loss: float, dt: float) -> float:
    return temperature + ((q_heat + q_solar + q_internal - q_loss) / heat_capacity) * dt

def build_parameter_records() -> list[ParameterRecord]:
    return [
        ParameterRecord("C", 10.0, "W yr m^-2 K^-1", "effective heat capacity", "Heat capacity must match the modeled reservoir."),
        ParameterRecord("F", 3.7, "W m^-2", "external forcing", "Forcing assumptions should be documented as historical, scenario-based, or experimental."),
        ParameterRecord("lambda", 1.2, "W m^-2 K^-1", "feedback parameter", "Feedback terms can hide multiple physical processes."),
        ParameterRecord("alpha", 0.30, "fraction", "albedo", "Albedo can vary with clouds, ice, land cover, and surface condition."),
        ParameterRecord("kappa", 0.7, "W m^-2 K^-1", "upper-deep layer exchange", "Layer exchange controls delayed response and hidden heat uptake."),
        ParameterRecord("S0", 1361.0, "W m^-2", "solar constant", "Solar input requires geometric averaging and boundary definition."),
    ]

def build_scenarios() -> list[ScenarioRecord]:
    years, dt = 150.0, 0.1
    steps = int(years / dt)
    base_eq = equilibrium_temperature(3.7, 1.2)
    base_tau = adjustment_time(10.0, 1.2)
    base_final = one_layer_response(3.7, 1.2, 10.0, 0.0, dt, steps)
    high_feedback_eq = equilibrium_temperature(3.7, 1.8)
    high_feedback_tau = adjustment_time(10.0, 1.8)
    high_feedback_final = one_layer_response(3.7, 1.8, 10.0, 0.0, dt, steps)
    high_capacity_tau = adjustment_time(40.0, 1.2)
    high_capacity_final = one_layer_response(3.7, 1.2, 40.0, 0.0, dt, steps)
    upper, deep = two_layer_response(3.7, 1.2, 0.7, 10.0, 100.0, 0.0, 0.0, dt, steps)
    return [
        ScenarioRecord("baseline_one_layer", "one_layer", years, base_final, base_eq, base_tau, "one-layer model approaches equilibrium according to heat capacity and feedback"),
        ScenarioRecord("stronger_feedback", "one_layer", years, high_feedback_final, high_feedback_eq, high_feedback_tau, "stronger feedback reduces equilibrium response and shortens adjustment time"),
        ScenarioRecord("larger_heat_capacity", "one_layer", years, high_capacity_final, base_eq, high_capacity_tau, "larger heat capacity slows transient response"),
        ScenarioRecord("two_layer_heat_uptake", "two_layer", years, upper, base_eq, base_tau, f"two-layer model stores heat in a slower reservoir; deep layer final temperature={deep:.3f}"),
    ]

def build_diagnostics() -> list[DiagnosticRecord]:
    return [
        DiagnosticRecord("absorbed_solar_example", absorbed_solar(1361.0, 0.30), "W m^-2", "absorbed solar radiation with geometric averaging", "Solar input requires albedo and geometry assumptions."),
        DiagnosticRecord("surface_storage_residual_example", surface_energy_partition(500.0, 120.0, 300.0, 40.0), "W m^-2", "storage residual after sensible, latent, and ground heat terms", "Omitted surface energy terms change storage interpretation."),
        DiagnosticRecord("building_temperature_step_example", building_temperature_step(20.0, 1000.0, 300.0, 150.0, 80.0, 420.0, 1.0), "degrees", "one-step building thermal balance", "Building thermal balance requires occupancy, weather, controls, and material assumptions."),
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
    parameters = [asdict(r) for r in build_parameter_records()]
    scenarios = [asdict(r) for r in build_scenarios()]
    diagnostics = [asdict(r) for r in build_diagnostics()]
    write_csv(output_dir/"tables"/"energy_parameter_records.csv", parameters)
    write_csv(output_dir/"tables"/"energy_scenario_records.csv", scenarios)
    write_csv(output_dir/"tables"/"energy_diagnostic_records.csv", diagnostics)
    audit = {
        "parameter_records": parameters,
        "scenario_records": scenarios,
        "diagnostics": diagnostics,
        "interpretation_warning": "Energy balance model outputs depend on system boundaries, energy-flow definitions, heat capacity, forcing assumptions, feedback structure, calibration data, uncertainty, and claim boundaries."
    }
    (output_dir/"json"/"energy_balance_audit.json").write_text(json.dumps(audit, indent=2, sort_keys=True), encoding="utf-8")
    report = ["# Energy Balance Model Audit", "", "## Scenario Records"]
    for row in scenarios:
        report.append(f"- **{row['scenario_name']}** ({row['model_type']}): final temperature={row['final_temperature']:.3f}, equilibrium={row['equilibrium_temperature']:.3f}, adjustment time={row['adjustment_time']:.3f}. {row['interpretation']}.")
    report += ["", "## Diagnostic Records"]
    for row in diagnostics:
        report.append(f"- **{row['diagnostic_name']}**: value={row['value']:.3f} {row['unit']}. {row['warning']}")
    (output_dir/"reports"/"energy_balance_audit.md").write_text("\n".join(report)+"\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Energy balance audit outputs generated.")

if __name__ == "__main__":
    main()
