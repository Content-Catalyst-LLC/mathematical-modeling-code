from __future__ import annotations
import argparse, csv, json, math, random
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class ParameterRecord:
    parameter_name: str
    value: float
    unit: str
    source_status: str
    interpretation: str
    warning: str

@dataclass(frozen=True)
class ScenarioRecord:
    scenario_name: str
    model_type: str
    final_time: float
    final_population: float
    interpretation: str

@dataclass(frozen=True)
class IdentifiabilityRecord:
    diagnostic_name: str
    issue: str
    warning: str
    governance_response: str

def exponential(n0: float, r: float, t: float) -> float:
    return n0 * math.exp(r * t)

def logistic(n0: float, r: float, k: float, t: float) -> float:
    return k / (1 + ((k - n0) / n0) * math.exp(-r * t))

def simulate(n0: float, derivative, dt: float, steps: int) -> float:
    n = n0
    for _ in range(steps):
        n = max(0.0, n + dt * derivative(n))
    return n

def allee_derivative(r: float, k: float, a: float):
    return lambda n: r * n * (1 - n / k) * (n / a - 1)

def harvest_derivative(r: float, k: float, h: float):
    return lambda n: r * n * (1 - n / k) - h

def stochastic_logistic(n0: float, r: float, k: float, sigma: float, dt: float, steps: int, seed: int = 17) -> float:
    rng = random.Random(seed)
    n = n0
    for _ in range(steps):
        n = max(0.0, n + r*n*(1-n/k)*dt + sigma*n*math.sqrt(dt)*rng.gauss(0, 1))
    return n

def two_patch(n1: float, n2: float, r: float, k: float, m: float, dt: float, steps: int) -> tuple[float, float]:
    for _ in range(steps):
        d1 = r*n1*(1-n1/k) + m*(n2-n1)
        d2 = r*n2*(1-n2/k) + m*(n1-n2)
        n1 = max(0.0, n1 + dt*d1)
        n2 = max(0.0, n2 + dt*d2)
    return n1, n2

def leslie_project(initial: list[float], matrix: list[list[float]], steps: int) -> list[float]:
    vector = initial[:]
    for _ in range(steps):
        vector = [sum(matrix[i][j] * vector[j] for j in range(len(vector))) for i in range(len(vector))]
    return vector

def diffusion_step(values: list[float], d: float, dt: float, dx: float) -> list[float]:
    out = values[:]
    coef = d * dt / (dx * dx)
    for i in range(1, len(values)-1):
        out[i] = values[i] + coef * (values[i-1] - 2*values[i] + values[i+1])
    return [max(0.0, v) for v in out]

def calibration_grid(observations: list[tuple[float, float]], n0: float) -> list[dict]:
    candidates = []
    for r in [0.04, 0.06, 0.08, 0.10, 0.12]:
        for k in [600, 800, 1000, 1200, 1500]:
            sse = sum((obs - logistic(n0, r, k, t))**2 for t, obs in observations)
            candidates.append({"r": r, "K": float(k), "sse": sse})
    return sorted(candidates, key=lambda row: row["sse"])[:8]

def parameters() -> list[ParameterRecord]:
    return [
        ParameterRecord("N0", 100, "individuals", "synthetic teaching value", "initial population", "Initial values should include uncertainty."),
        ParameterRecord("r", 0.08, "per year", "synthetic teaching value", "intrinsic growth rate", "Growth rates may vary across conditions."),
        ParameterRecord("K", 1000, "individuals", "synthetic teaching value", "carrying capacity", "Carrying capacity may change over time."),
        ParameterRecord("A", 75, "individuals", "synthetic teaching value", "Allee threshold", "Threshold parameters can be hard to identify."),
        ParameterRecord("H", 12, "individuals per year", "synthetic teaching value", "harvest/removal rate", "Removal terms are management assumptions."),
        ParameterRecord("sigma", 0.12, "noise intensity", "synthetic teaching value", "environmental variability", "Stochastic output should be summarized as distribution."),
        ParameterRecord("m", 0.04, "per year", "synthetic teaching value", "migration coefficient", "Movement assumptions should match spatial context."),
    ]

def scenarios() -> list[ScenarioRecord]:
    n0, r, k, t, dt = 100.0, 0.08, 1000.0, 40.0, 0.1
    steps = int(t/dt)
    p1, p2 = two_patch(100, 400, r, k, 0.04, dt, steps)
    structured = leslie_project([80.0, 40.0, 20.0], [[0.0,1.2,1.8],[0.55,0.0,0.0],[0.0,0.65,0.30]], 20)
    spatial = diffusion_step([20, 40, 300, 40, 20], 0.03, 0.1, 1.0)
    return [
        ScenarioRecord("exponential_baseline", "exponential", t, exponential(n0, r, t), "unconstrained baseline"),
        ScenarioRecord("logistic_capacity_limited", "logistic", t, logistic(n0, r, k, t), "capacity-limited baseline"),
        ScenarioRecord("allee_threshold", "allee_effect", t, simulate(n0, allee_derivative(r, k, 75), dt, steps), "low-population threshold"),
        ScenarioRecord("harvesting_pressure", "harvesting", t, simulate(n0, harvest_derivative(r, k, 12), dt, steps), "external removal pressure"),
        ScenarioRecord("stochastic_logistic_path", "stochastic", t, stochastic_logistic(n0, r, k, 0.12, dt, steps), "one stochastic path"),
        ScenarioRecord("two_patch_total", "metapopulation", t, p1+p2, "two connected patches"),
        ScenarioRecord("structured_total", "leslie_matrix", 20, sum(structured), "stage-structured projection"),
        ScenarioRecord("spatial_grid_total", "diffusion_step", 0.1, sum(spatial), "one spatial diffusion update"),
    ]

def identifiability() -> list[IdentifiabilityRecord]:
    return [
        IdentifiabilityRecord("short_series_r_k_tradeoff", "Different r and K values can fit early growth similarly.", "Do not infer carrying capacity from short early-growth data alone.", "Use profile likelihood, grid search, or longer time series."),
        IdentifiabilityRecord("threshold_parameter_A", "Allee thresholds may be invisible unless data include low-population behavior.", "Threshold claims need evidence near the threshold.", "Run threshold scenarios and state uncertainty."),
        IdentifiabilityRecord("stochastic_sigma", "Noise intensity depends on what variability is represented.", "A single stochastic path is not a distribution.", "Summarize ensembles, quantiles, and extinction probability."),
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
    pr = [asdict(row) for row in parameters()]
    sc = [asdict(row) for row in scenarios()]
    idr = [asdict(row) for row in identifiability()]
    grid = calibration_grid([(0,100), (10,180), (20,320), (30,500)], 100.0)
    write_csv(output_dir/"tables"/"population_parameter_records.csv", pr)
    write_csv(output_dir/"tables"/"population_advanced_scenario_records.csv", sc)
    write_csv(output_dir/"tables"/"population_identifiability_records.csv", idr)
    write_csv(output_dir/"tables"/"population_calibration_grid_top.csv", grid)
    audit = {"parameter_records": pr, "scenario_records": sc, "identifiability_records": idr, "calibration_grid_top": grid, "interpretation_warning": "Population model outputs depend on growth-law assumptions, parameter evidence, scope, omitted mechanisms, stochasticity, structure, and spatial context."}
    (output_dir/"json"/"advanced_population_dynamics_audit.json").write_text(json.dumps(audit, indent=2, sort_keys=True), encoding="utf-8")
    report = ["# Advanced Population Dynamics Audit", "", "## Scenarios"]
    for row in sc:
        report.append(f"- **{row['scenario_name']}** ({row['model_type']}): final value {row['final_population']:.2f}. {row['interpretation']}.")
    report += ["", "## Identifiability Warnings"]
    for row in idr:
        report.append(f"- **{row['diagnostic_name']}**: {row['warning']} Response: {row['governance_response']}")
    (output_dir/"reports"/"advanced_population_dynamics_audit.md").write_text("\n".join(report)+"\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced population dynamics outputs generated.")

if __name__ == "__main__":
    main()
