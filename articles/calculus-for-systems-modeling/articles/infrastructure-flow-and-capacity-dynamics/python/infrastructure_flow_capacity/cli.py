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
    system_type: str
    final_time: float
    final_queue: float
    average_utilization: float
    maximum_delay: float
    interpretation: str

@dataclass(frozen=True)
class BottleneckRecord:
    record_name: str
    stage_capacities: str
    effective_capacity: float
    bottleneck_stage: int
    warning: str

def utilization(arrival_rate: float, capacity: float) -> float:
    if capacity <= 0:
        raise ValueError("capacity must be positive")
    return arrival_rate / capacity

def delay_function(utilization_value: float, base_delay: float = 1.0, alpha: float = 0.8) -> float:
    if utilization_value >= 1.0:
        return float("inf")
    return base_delay * (1 + alpha * (utilization_value / (1 - utilization_value)))

def simulate_queue(arrival_rate: float, service_capacity: float, dt: float, steps: int, initial_queue: float = 0.0) -> tuple[float, float, float]:
    queue = initial_queue
    total_utilization = 0.0
    maximum_delay = 0.0
    for _ in range(steps):
        served = min(queue + arrival_rate * dt, service_capacity * dt)
        queue = max(0.0, queue + arrival_rate * dt - served)
        u = utilization(arrival_rate, service_capacity)
        total_utilization += u
        d = delay_function(min(u, 0.999))
        maximum_delay = max(maximum_delay, d)
    return queue, total_utilization / steps, maximum_delay

def effective_capacity(capacities: list[float]) -> float:
    return min(capacities)

def bottleneck_stage(capacities: list[float]) -> int:
    return capacities.index(min(capacities)) + 1

def simulate_buffer(inflow: float, outflow: float, buffer_capacity: float, dt: float, steps: int) -> tuple[float, bool]:
    buffer = 0.0
    saturated = False
    for _ in range(steps):
        buffer += (inflow - outflow) * dt
        if buffer >= buffer_capacity:
            buffer = buffer_capacity
            saturated = True
        buffer = max(0.0, buffer)
    return buffer, saturated

def capacity_after_decay(initial_capacity: float, maintenance: float, decay_rate: float, dt: float, steps: int) -> float:
    capacity = initial_capacity
    for _ in range(steps):
        capacity = max(0.0, capacity + maintenance * dt - decay_rate * capacity * dt)
    return capacity

def service_resilience_ratio(service_delivered: float, service_required: float) -> float:
    return service_delivered / service_required if service_required else 0.0

def build_parameter_records() -> list[ParameterRecord]:
    return [
        ParameterRecord("lambda", 95.0, "units per hour", "arrival or demand rate", "Peak and average demand should be documented separately."),
        ParameterRecord("mu", 100.0, "units per hour", "service capacity", "Nominal capacity may differ from effective capacity."),
        ParameterRecord("buffer_capacity", 300.0, "units", "maximum buffer or storage capacity", "Buffers can saturate under sustained imbalance."),
        ParameterRecord("base_delay", 1.0, "time units", "delay under low utilization", "Delay rises nonlinearly near capacity."),
        ParameterRecord("decay_rate", 0.03, "per year", "capacity decay rate", "Capacity should not be assumed fixed without maintenance records."),
        ParameterRecord("recovery_rate", 0.15, "per period", "post-disruption recovery rate", "Recovery depends on labor, parts, finance, and governance."),
        ParameterRecord("peak_multiplier", 1.25, "factor", "peak-load multiplier", "Average demand can hide peak stress."),
    ]

def build_scenarios() -> list[ScenarioRecord]:
    dt = 0.1
    t = 24.0
    steps = int(t / dt)

    baseline_queue, baseline_utilization, baseline_delay = simulate_queue(75.0, 100.0, dt, steps)
    near_capacity_queue, near_capacity_utilization, near_capacity_delay = simulate_queue(95.0, 100.0, dt, steps)
    overload_queue, overload_utilization, overload_delay = simulate_queue(115.0, 100.0, dt, steps)

    bottleneck_cap = effective_capacity([140.0, 120.0, 90.0, 130.0])
    bottleneck_queue, bottleneck_utilization, bottleneck_delay = simulate_queue(95.0, bottleneck_cap, dt, steps)

    decayed_capacity = capacity_after_decay(100.0, 1.5, 0.03, 1.0, 20)
    decayed_queue, decayed_utilization, decayed_delay = simulate_queue(95.0, decayed_capacity, dt, steps)

    peak_queue, peak_utilization, peak_delay = simulate_queue(95.0 * 1.25, 125.0, dt, steps)

    return [
        ScenarioRecord("baseline_spare_capacity", "queue_capacity", t, baseline_queue, baseline_utilization, baseline_delay, "spare capacity keeps queues low"),
        ScenarioRecord("near_capacity_operation", "queue_capacity", t, near_capacity_queue, near_capacity_utilization, near_capacity_delay, "near-capacity operation creates high delay sensitivity"),
        ScenarioRecord("over_capacity_backlog", "queue_capacity", t, overload_queue, overload_utilization, overload_delay, "arrival rate above capacity causes backlog accumulation"),
        ScenarioRecord("series_bottleneck", "network_bottleneck", t, bottleneck_queue, bottleneck_utilization, bottleneck_delay, "minimum stage capacity limits effective throughput"),
        ScenarioRecord("capacity_decay_case", "maintenance_capacity", t, decayed_queue, decayed_utilization, decayed_delay, "capacity decay can create congestion even if demand is unchanged"),
        ScenarioRecord("peak_load_case", "peak_load_capacity", t, peak_queue, peak_utilization, peak_delay, "peak-load scenario tests stress conditions beyond average demand"),
    ]

def build_bottleneck_records() -> list[BottleneckRecord]:
    capacities = [140.0, 120.0, 90.0, 130.0]
    return [
        BottleneckRecord(
            "series_process_bottleneck",
            ",".join(str(x) for x in capacities),
            effective_capacity(capacities),
            bottleneck_stage(capacities),
            "Effective capacity is limited by the smallest stage capacity."
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
    bottlenecks = [asdict(record) for record in build_bottleneck_records()]

    write_csv(output_dir/"tables"/"infrastructure_parameter_records.csv", parameters)
    write_csv(output_dir/"tables"/"infrastructure_scenario_records.csv", scenarios)
    write_csv(output_dir/"tables"/"infrastructure_bottleneck_records.csv", bottlenecks)

    audit = {
        "parameter_records": parameters,
        "scenario_records": scenarios,
        "bottleneck_records": bottlenecks,
        "interpretation_warning": "Infrastructure model outputs depend on flow definitions, effective capacity, queues, bottlenecks, buffers, maintenance, failure modes, recovery assumptions, uncertainty, and claim boundaries."
    }
    (output_dir/"json"/"infrastructure_flow_capacity_audit.json").write_text(json.dumps(audit, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Infrastructure Flow and Capacity Audit", "", "## Scenario Records"]
    for row in scenarios:
        report.append(f"- **{row['scenario_name']}** ({row['system_type']}): final queue={row['final_queue']:.2f}, average utilization={row['average_utilization']:.3f}, maximum delay={row['maximum_delay']:.2f}. {row['interpretation']}.")
    report += ["", "## Bottleneck Records"]
    for row in bottlenecks:
        report.append(f"- **{row['record_name']}**: effective capacity={row['effective_capacity']:.2f}; bottleneck stage={row['bottleneck_stage']}. {row['warning']}")
    report.append("")
    report.append("Infrastructure model outputs depend on flow definitions, effective capacity, queues, bottlenecks, buffers, maintenance, failure modes, recovery assumptions, uncertainty, and claim boundaries.")
    (output_dir/"reports"/"infrastructure_flow_capacity_audit.md").write_text("\n".join(report)+"\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Infrastructure flow and capacity audit outputs generated.")

if __name__ == "__main__":
    main()
