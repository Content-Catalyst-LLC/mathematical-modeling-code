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
    peak_infectious: float
    final_recovered: float
    reproduction_number: float
    interpretation: str

@dataclass(frozen=True)
class ThresholdRecord:
    record_name: str
    r0: float
    susceptible_threshold: float
    herd_immunity_threshold: float
    doubling_time: float
    warning: str

def basic_reproduction_number(beta: float, gamma: float) -> float:
    if gamma <= 0:
        raise ValueError("gamma must be positive")
    return beta / gamma

def effective_reproduction_number(beta: float, gamma: float, susceptible: float, population: float) -> float:
    return basic_reproduction_number(beta, gamma) * (susceptible / population)

def doubling_time(growth_rate: float) -> float:
    if growth_rate <= 0:
        return math.inf
    return math.log(2) / growth_rate

def herd_immunity_threshold(r0: float) -> float:
    if r0 <= 0:
        return 0.0
    return max(0.0, 1 - 1 / r0)

def force_of_infection(beta: float, infectious: float, population: float) -> float:
    return beta * infectious / population

def incidence(beta: float, susceptible: float, infectious: float, population: float) -> float:
    return beta * susceptible * infectious / population

def simulate_sir(population: float, susceptible0: float, infectious0: float, recovered0: float, beta: float, gamma: float, dt: float, steps: int) -> tuple[float, float, float, float]:
    s = susceptible0
    i = infectious0
    r = recovered0
    peak_i = i
    for _ in range(steps):
        new_inf = incidence(beta, s, i, population)
        recovery = gamma * i
        s = max(0.0, s - new_inf * dt)
        i = max(0.0, i + (new_inf - recovery) * dt)
        r = min(population, r + recovery * dt)
        peak_i = max(peak_i, i)
    return s, i, r, peak_i

def simulate_seir(population: float, susceptible0: float, exposed0: float, infectious0: float, recovered0: float, beta: float, sigma: float, gamma: float, dt: float, steps: int) -> tuple[float, float, float, float, float]:
    s = susceptible0
    e = exposed0
    i = infectious0
    r = recovered0
    peak_i = i
    for _ in range(steps):
        new_inf = incidence(beta, s, i, population)
        progression = sigma * e
        recovery = gamma * i
        s = max(0.0, s - new_inf * dt)
        e = max(0.0, e + (new_inf - progression) * dt)
        i = max(0.0, i + (progression - recovery) * dt)
        r = min(population, r + recovery * dt)
        peak_i = max(peak_i, i)
    return s, e, i, r, peak_i

def vaccination_waning_step(s: float, v: float, vaccination_rate: float, waning_rate: float, dt: float) -> tuple[float, float]:
    vaccinated = vaccination_rate * s * dt
    waned = waning_rate * v * dt
    return max(0.0, s - vaccinated + waned), max(0.0, v + vaccinated - waned)

def build_parameter_records() -> list[ParameterRecord]:
    return [
        ParameterRecord("N", 100000.0, "people", "population boundary", "Population boundary and mixing assumptions must be documented."),
        ParameterRecord("beta", 0.32, "per day", "transmission parameter", "Transmission combines contact, infectiousness, behavior, setting, and reporting context."),
        ParameterRecord("gamma", 0.10, "per day", "recovery or removal rate", "Recovery rate should be tied to infectious period assumptions."),
        ParameterRecord("sigma", 0.20, "per day", "progression from exposed to infectious", "Latency and incubation assumptions should be distinguished where needed."),
        ParameterRecord("nu", 0.005, "per day", "vaccination rate", "Vaccination assumptions require coverage, timing, efficacy, and equity records."),
        ParameterRecord("omega", 0.001, "per day", "waning protection rate", "Waning immunity assumptions can change long-run dynamics."),
        ParameterRecord("rho", 0.50, "fraction", "reporting or detection fraction", "Reported cases should not be treated as true infections without observation assumptions."),
    ]

def build_scenarios() -> list[ScenarioRecord]:
    population = 100000.0
    dt = 0.1
    days = 160.0
    steps = int(days / dt)

    r0_baseline = basic_reproduction_number(0.32, 0.10)
    s, i, r, peak = simulate_sir(population, 99900.0, 100.0, 0.0, 0.32, 0.10, dt, steps)

    r0_reduced = basic_reproduction_number(0.22, 0.10)
    s2, i2, r2, peak2 = simulate_sir(population, 99900.0, 100.0, 0.0, 0.22, 0.10, dt, steps)

    r0_seir = basic_reproduction_number(0.32, 0.10)
    s3, e3, i3, r3, peak3 = simulate_seir(population, 99850.0, 50.0, 100.0, 0.0, 0.32, 0.20, 0.10, dt, steps)

    vaccination_susceptible = 85000.0
    rt_vaccination = effective_reproduction_number(0.32, 0.10, vaccination_susceptible, population)
    s4, i4, r4, peak4 = simulate_sir(population, vaccination_susceptible, 100.0, population - vaccination_susceptible - 100.0, 0.32, 0.10, dt, steps)

    return [
        ScenarioRecord("baseline_sir", "SIR", days, peak, r, r0_baseline, "baseline SIR scenario with susceptible depletion"),
        ScenarioRecord("reduced_transmission_sir", "SIR", days, peak2, r2, r0_reduced, "lower transmission reduces peak infectious burden"),
        ScenarioRecord("latent_period_seir", "SEIR", days, peak3, r3, r0_seir, "exposed compartment delays infectious growth"),
        ScenarioRecord("vaccination_reduced_susceptible", "SIR_vaccination", days, peak4, r4, rt_vaccination, "lower susceptible share reduces effective reproduction number"),
    ]

def build_threshold_records() -> list[ThresholdRecord]:
    r0 = basic_reproduction_number(0.32, 0.10)
    growth_rate = 0.32 - 0.10
    return [
        ThresholdRecord(
            "baseline_thresholds",
            r0,
            1 / r0,
            herd_immunity_threshold(r0),
            doubling_time(growth_rate),
            "Thresholds are model-dependent summaries and should be presented with assumptions and context."
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
    thresholds = [asdict(record) for record in build_threshold_records()]

    write_csv(output_dir/"tables"/"epidemiological_parameter_records.csv", parameters)
    write_csv(output_dir/"tables"/"epidemiological_scenario_records.csv", scenarios)
    write_csv(output_dir/"tables"/"epidemiological_threshold_records.csv", thresholds)

    audit = {
        "parameter_records": parameters,
        "scenario_records": scenarios,
        "threshold_records": thresholds,
        "interpretation_warning": "Epidemiological model outputs depend on compartment definitions, population boundaries, transmission assumptions, reporting processes, initial conditions, intervention mechanisms, uncertainty, and claim boundaries."
    }
    (output_dir/"json"/"continuous_time_epidemiology_audit.json").write_text(json.dumps(audit, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Continuous-Time Epidemiological Model Audit", "", "## Scenario Records"]
    for row in scenarios:
        report.append(f"- **{row['scenario_name']}** ({row['model_type']}): peak infectious={row['peak_infectious']:.2f}, final recovered={row['final_recovered']:.2f}, reproduction number={row['reproduction_number']:.3f}. {row['interpretation']}.")
    report += ["", "## Threshold Records"]
    for row in thresholds:
        report.append(f"- **{row['record_name']}**: R0={row['r0']:.3f}; susceptible threshold={row['susceptible_threshold']:.3f}; herd-immunity threshold={row['herd_immunity_threshold']:.3f}; doubling time={row['doubling_time']:.2f}. {row['warning']}")
    report.append("")
    report.append("Epidemiological model outputs depend on compartment definitions, population boundaries, transmission assumptions, reporting processes, initial conditions, intervention mechanisms, uncertainty, and claim boundaries.")
    (output_dir/"reports"/"continuous_time_epidemiology_audit.md").write_text("\n".join(report)+"\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Continuous-time epidemiological audit outputs generated.")

if __name__ == "__main__":
    main()
