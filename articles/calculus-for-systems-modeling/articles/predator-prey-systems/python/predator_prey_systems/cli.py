from __future__ import annotations
import argparse, csv, json, math, random
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
    final_prey: float
    final_predator: float
    interpretation: str

@dataclass(frozen=True)
class NullclineRecord:
    nullcline_name: str
    equation: str
    interpretation: str
    warning: str

@dataclass(frozen=True)
class StabilityRecord:
    equilibrium_name: str
    prey_value: float
    predator_value: float
    trace: float
    determinant: float
    local_status: str
    warning: str

def lotka_volterra_derivative(alpha: float, beta: float, gamma: float, delta: float):
    def derivative(x: float, y: float) -> tuple[float, float]:
        return alpha * x - beta * x * y, delta * x * y - gamma * y
    return derivative

def logistic_prey_derivative(r: float, k: float, beta: float, gamma: float, delta: float):
    def derivative(x: float, y: float) -> tuple[float, float]:
        return r * x * (1 - x / k) - beta * x * y, delta * x * y - gamma * y
    return derivative

def type_ii_derivative(r: float, k: float, a: float, h: float, gamma: float, delta: float):
    def derivative(x: float, y: float) -> tuple[float, float]:
        predation = (a * x * y) / (1 + a * h * x)
        return r * x * (1 - x / k) - predation, delta * predation - gamma * y
    return derivative

def harvesting_derivative(alpha: float, beta: float, gamma: float, delta: float, hx: float, hy: float):
    def derivative(x: float, y: float) -> tuple[float, float]:
        return alpha * x - beta * x * y - hx, delta * x * y - gamma * y - hy
    return derivative

def simulate_pair(x0: float, y0: float, derivative, dt: float, steps: int) -> tuple[float, float]:
    x, y = x0, y0
    for _ in range(steps):
        dx, dy = derivative(x, y)
        x = max(0.0, x + dt * dx)
        y = max(0.0, y + dt * dy)
    return x, y

def stochastic_pair(x0: float, y0: float, derivative, sigma_x: float, sigma_y: float, dt: float, steps: int, seed: int = 11) -> tuple[float, float]:
    rng = random.Random(seed)
    x, y = x0, y0
    for _ in range(steps):
        dx, dy = derivative(x, y)
        x = max(0.0, x + dt * dx + sigma_x * x * math.sqrt(dt) * rng.gauss(0, 1))
        y = max(0.0, y + dt * dy + sigma_y * y * math.sqrt(dt) * rng.gauss(0, 1))
    return x, y

def jacobian_lotka_volterra(alpha: float, beta: float, gamma: float, delta: float, x: float, y: float) -> tuple[float, float, float, float]:
    return alpha - beta * y, -beta * x, delta * y, delta * x - gamma

def trace_det(j: tuple[float, float, float, float]) -> tuple[float, float]:
    a, b, c, d = j
    return a + d, a * d - b * c

def stability_status(trace: float, determinant: float) -> str:
    if determinant < 0:
        return "saddle"
    if determinant > 0 and abs(trace) < 1e-9:
        return "center_or_neutral_linearization"
    if determinant > 0 and trace < 0:
        return "locally_stable"
    if determinant > 0 and trace > 0:
        return "locally_unstable"
    return "degenerate_or_requires_review"

def build_parameter_records() -> list[ParameterRecord]:
    return [
        ParameterRecord("alpha", 0.6, "per year", "prey intrinsic growth rate", "Prey growth may be resource-limited rather than exponential."),
        ParameterRecord("beta", 0.02, "encounter coefficient", "predation interaction coefficient", "Mass-action encounters may overstate interaction in spatial systems."),
        ParameterRecord("gamma", 0.5, "per year", "predator mortality rate", "Mortality may vary by age, season, or environment."),
        ParameterRecord("delta", 0.01, "conversion coefficient", "conversion from prey encounters to predator growth", "Conversion efficiency should not be treated as mechanism without evidence."),
        ParameterRecord("K", 500.0, "prey units", "prey carrying capacity", "Carrying capacity is assumption-bearing and may change over time."),
        ParameterRecord("h", 0.08, "time per prey", "handling time", "Saturation claims require evidence for functional response."),
    ]

def build_nullcline_records() -> list[NullclineRecord]:
    return [
        NullclineRecord("prey_nullcline", "dx/dt = 0 -> x = 0 or y = alpha / beta", "Prey stop changing when predator abundance balances prey growth.", "The nullcline depends on mass-action assumptions."),
        NullclineRecord("predator_nullcline", "dy/dt = 0 -> y = 0 or x = gamma / delta", "Predators stop changing when prey abundance balances mortality.", "The nullcline depends on conversion and mortality assumptions."),
        NullclineRecord("coexistence_equilibrium", "(x*, y*) = (gamma/delta, alpha/beta)", "Coexistence occurs where both populations have zero instantaneous growth.", "Equilibrium is a mathematical condition, not a full ecological conclusion."),
    ]

def build_stability_records() -> list[StabilityRecord]:
    alpha, beta, gamma, delta = 0.6, 0.02, 0.5, 0.01
    x_star = gamma / delta
    y_star = alpha / beta
    tr, det = trace_det(jacobian_lotka_volterra(alpha, beta, gamma, delta, x_star, y_star))
    return [
        StabilityRecord(
            "lotka_volterra_coexistence",
            x_star,
            y_star,
            tr,
            det,
            stability_status(tr, det),
            "Classic Lotka-Volterra neutral-cycle behavior depends on ideal assumptions."
        )
    ]

def build_scenarios() -> list[ScenarioRecord]:
    x0, y0 = 40.0, 9.0
    dt = 0.02
    t = 80.0
    steps = int(t / dt)

    cases = [
        ("classic_lotka_volterra", "lotka_volterra", lotka_volterra_derivative(0.6, 0.02, 0.5, 0.01), "baseline mass-action predator-prey interaction"),
        ("logistic_prey_limit", "logistic_prey", logistic_prey_derivative(0.6, 500.0, 0.02, 0.5, 0.01), "prey growth limited by carrying capacity"),
        ("type_ii_functional_response", "saturating_predation", type_ii_derivative(0.6, 500.0, 0.04, 0.08, 0.5, 0.4), "predation saturates due to handling time"),
        ("harvesting_pressure", "harvesting", harvesting_derivative(0.6, 0.02, 0.5, 0.01, 1.0, 0.05), "external removal shifts dynamics and risk"),
    ]

    scenarios = []
    for name, model_type, derivative, note in cases:
        x, y = simulate_pair(x0, y0, derivative, dt, steps)
        scenarios.append(ScenarioRecord(name, model_type, t, x, y, note))

    x, y = stochastic_pair(x0, y0, lotka_volterra_derivative(0.6, 0.02, 0.5, 0.01), 0.08, 0.08, dt, steps)
    scenarios.append(ScenarioRecord("stochastic_lotka_volterra_path", "stochastic", t, x, y, "one stochastic path under environmental variability"))
    return scenarios

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
    nullclines = [asdict(record) for record in build_nullcline_records()]
    stability = [asdict(record) for record in build_stability_records()]

    write_csv(output_dir/"tables"/"predator_prey_parameter_records.csv", parameters)
    write_csv(output_dir/"tables"/"predator_prey_scenario_records.csv", scenarios)
    write_csv(output_dir/"tables"/"predator_prey_nullcline_records.csv", nullclines)
    write_csv(output_dir/"tables"/"predator_prey_stability_records.csv", stability)

    audit = {
        "parameter_records": parameters,
        "scenario_records": scenarios,
        "nullcline_records": nullclines,
        "stability_records": stability,
        "interpretation_warning": "Predator-prey model outputs depend on interaction assumptions, functional response, parameter evidence, stochasticity, spatial structure, and claim boundaries.",
    }
    (output_dir/"json"/"predator_prey_dynamics_audit.json").write_text(json.dumps(audit, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Predator-Prey Dynamics Model Audit", "", "## Scenario Records"]
    for row in scenarios:
        report.append(f"- **{row['scenario_name']}** ({row['model_type']}): prey={row['final_prey']:.2f}, predator={row['final_predator']:.2f}. {row['interpretation']}.")
    report += ["", "## Stability Records"]
    for row in stability:
        report.append(f"- **{row['equilibrium_name']}**: trace={row['trace']:.4f}, determinant={row['determinant']:.4f}, status={row['local_status']}. {row['warning']}")
    report.append("")
    report.append("Predator-prey model outputs depend on interaction assumptions, functional response, parameter evidence, stochasticity, spatial structure, and claim boundaries.")
    (output_dir/"reports"/"predator_prey_dynamics_audit.md").write_text("\n".join(report)+"\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Predator-prey dynamics audit outputs generated.")

if __name__ == "__main__":
    main()
