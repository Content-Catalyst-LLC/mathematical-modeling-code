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
    demand: float
    capacity: float
    final_queue: float
    total_delay: float
    travel_time: float
    interpretation: str

@dataclass(frozen=True)
class DiagnosticRecord:
    diagnostic_name: str
    value: float
    unit: str
    interpretation: str
    warning: str

def traffic_flow(density: float, free_flow_speed: float, jam_density: float) -> float:
    return max(0.0, free_flow_speed * density * (1 - density / jam_density))

def critical_density(jam_density: float) -> float:
    return jam_density / 2

def queue_step(queue: float, arrival_rate: float, service_rate: float, dt: float) -> float:
    return max(0.0, queue + (arrival_rate - service_rate) * dt)

def simulate_queue(arrival_rate: float, service_rate: float, duration: float, dt: float) -> tuple[float, float]:
    queue = 0.0
    total_delay = 0.0
    steps = int(duration / dt)
    for _ in range(steps):
        queue = queue_step(queue, arrival_rate, service_rate, dt)
        total_delay += queue * dt
    return queue, total_delay

def bpr_travel_time(free_flow_time: float, volume: float, capacity: float, alpha: float = 0.15, beta: float = 4.0) -> float:
    if capacity <= 0:
        raise ValueError("capacity must be positive")
    return free_flow_time * (1 + alpha * (volume / capacity) ** beta)

def accessibility(opportunities: list[float], travel_times: list[float], theta: float) -> float:
    return sum(o * math.exp(-theta * t) for o, t in zip(opportunities, travel_times))

def induced_demand_step(volume: float, target_volume: float, adjustment_rate: float, dt: float) -> float:
    return volume + adjustment_rate * (target_volume - volume) * dt

def distributional_delay_burden(delays: list[float], weights: list[float]) -> float:
    return sum(delay * weight for delay, weight in zip(delays, weights))

def curb_occupancy_step(occupied: float, use_rate: float, release_rate: float, capacity: float, dt: float) -> float:
    return min(capacity, max(0.0, occupied + (use_rate - release_rate) * dt))

def build_parameter_records() -> list[ParameterRecord]:
    return [
        ParameterRecord("q", 1800.0, "vehicles per hour", "traffic flow", "Flow unit and mode must be documented."),
        ParameterRecord("k", 35.0, "vehicles per kilometer", "density", "Density depends on vehicle mix, lane definition, and measurement method."),
        ParameterRecord("v_f", 60.0, "kilometers per hour", "free-flow speed", "Free-flow speed should not be treated as a universal target."),
        ParameterRecord("k_j", 140.0, "vehicles per kilometer", "jam density", "Jam density represents near-standstill conditions."),
        ParameterRecord("C", 2000.0, "vehicles per hour", "capacity", "Capacity depends on design, signals, incidents, weather, and curb use."),
        ParameterRecord("mu", 0.10, "per year", "demand adjustment rate", "Long-run demand can change after capacity or accessibility changes."),
        ParameterRecord("theta", 0.08, "per minute", "accessibility decay", "Accessibility assumptions shape equity interpretation."),
    ]

def build_scenarios() -> list[ScenarioRecord]:
    free_flow_time = 20.0
    duration = 3.0
    dt = 0.01

    queue_a, delay_a = simulate_queue(1800.0, 2000.0, duration, dt)
    tt_a = bpr_travel_time(free_flow_time, 1800.0, 2000.0)

    queue_b, delay_b = simulate_queue(2300.0, 2000.0, duration, dt)
    tt_b = bpr_travel_time(free_flow_time, 2300.0, 2000.0)

    queue_c, delay_c = simulate_queue(2300.0, 2600.0, duration, dt)
    induced_volume = 2300.0
    for _ in range(10):
        induced_volume = induced_demand_step(induced_volume, 2600.0, 0.15, 1.0)
    tt_c = bpr_travel_time(free_flow_time, induced_volume, 2600.0)

    queue_d, delay_d = simulate_queue(1200.0, 1600.0, duration, dt)
    tt_d = bpr_travel_time(free_flow_time, 1200.0, 1600.0)

    return [
        ScenarioRecord("below_capacity_corridor", "queue_and_bpr", 1800.0, 2000.0, queue_a, delay_a, tt_a, "demand below capacity produces limited queue accumulation"),
        ScenarioRecord("over_capacity_bottleneck", "queue_and_bpr", 2300.0, 2000.0, queue_b, delay_b, tt_b, "demand above capacity produces persistent queue and delay"),
        ScenarioRecord("capacity_expansion_with_induced_demand", "capacity_adjustment", induced_volume, 2600.0, queue_c, delay_c, tt_c, "capacity expansion may reduce delay while long-run demand adjusts upward"),
        ScenarioRecord("transit_priority_case", "multimodal_capacity", 1200.0, 1600.0, queue_d, delay_d, tt_d, "transit priority can reduce person-delay when person throughput is considered"),
    ]

def build_diagnostics() -> list[DiagnosticRecord]:
    return [
        DiagnosticRecord("critical_density_example", critical_density(140.0), "vehicles per kilometer", "density at maximum flow in simple parabolic model", "Critical density depends on the selected flow-density relation."),
        DiagnosticRecord("flow_at_density_example", traffic_flow(35.0, 60.0, 140.0), "vehicles per hour", "flow estimated from density, free-flow speed, and jam density", "Fundamental diagrams are context-specific, not universal laws."),
        DiagnosticRecord("accessibility_example", accessibility([1000, 500, 250], [10, 25, 45], 0.08), "weighted opportunities", "accessibility from opportunities and travel times", "Accessibility depends on opportunity definition and travel-cost assumptions."),
        DiagnosticRecord("distributional_delay_burden_example", distributional_delay_burden([10, 20, 35], [1.0, 1.5, 2.0]), "weighted minutes", "delay burden weighted across groups", "Average delay can hide unequal burden."),
        DiagnosticRecord("curb_occupancy_step_example", curb_occupancy_step(18.0, 10.0, 6.0, 20.0, 0.25), "occupied spaces", "curb occupancy after use and release", "Curb dynamics can reduce effective road and transit capacity."),
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

    write_csv(output_dir/"tables"/"urban_parameter_records.csv", parameters)
    write_csv(output_dir/"tables"/"urban_scenario_records.csv", scenarios)
    write_csv(output_dir/"tables"/"urban_diagnostic_records.csv", diagnostics)

    audit = {
        "parameter_records": parameters,
        "scenario_records": scenarios,
        "diagnostics": diagnostics,
        "interpretation_warning": "Urban congestion model outputs depend on system boundaries, flow definitions, capacity assumptions, behavioral response, mode options, land-use feedback, equity outputs, uncertainty, and claim boundaries."
    }
    (output_dir/"json"/"urban_dynamics_congestion_audit.json").write_text(json.dumps(audit, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Urban Dynamics and Congestion Audit", "", "## Scenario Records"]
    for row in scenarios:
        report.append(f"- **{row['scenario_name']}** ({row['model_type']}): demand={row['demand']:.1f}, capacity={row['capacity']:.1f}, final queue={row['final_queue']:.2f}, total delay={row['total_delay']:.2f}, travel time={row['travel_time']:.2f}. {row['interpretation']}.")
    report += ["", "## Diagnostic Records"]
    for row in diagnostics:
        report.append(f"- **{row['diagnostic_name']}**: {row['value']:.3f} {row['unit']}. {row['warning']}")
    report.append("")
    report.append("Urban congestion model outputs depend on system boundaries, flow definitions, capacity assumptions, behavioral response, mode options, land-use feedback, equity outputs, uncertainty, and claim boundaries.")
    (output_dir/"reports"/"urban_dynamics_congestion_audit.md").write_text("\n".join(report)+"\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Urban dynamics and congestion audit outputs generated.")

if __name__ == "__main__":
    main()
