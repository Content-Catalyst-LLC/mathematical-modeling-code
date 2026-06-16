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
    resource_type: str
    final_time: float
    final_stock: float
    cumulative_extraction: float
    interpretation: str

@dataclass(frozen=True)
class YieldRecord:
    record_name: str
    regeneration_rate: float
    carrying_capacity: float
    maximum_sustainable_yield: float
    precautionary_yield: float
    warning: str

def logistic_regeneration(stock: float, r: float, k: float) -> float:
    return max(0.0, r * stock * (1 - stock / k))

def threshold_regeneration(stock: float, r: float, k: float, threshold: float) -> float:
    return r * stock * (1 - stock / k) * (stock / threshold - 1)

def maximum_sustainable_yield(r: float, k: float) -> float:
    return r * k / 4.0

def simulate_resource(stock0: float, regeneration, harvest: float, dt: float, steps: int, loss_rate: float = 0.0) -> tuple[float, float]:
    stock = stock0
    cumulative_extraction = 0.0
    for _ in range(steps):
        extraction = min(stock, harvest * dt)
        growth = regeneration(stock) * dt
        loss = max(0.0, loss_rate * stock * dt)
        stock = max(0.0, stock + growth - extraction - loss)
        cumulative_extraction += extraction
    return stock, cumulative_extraction

def simulate_nonrenewable(stock0: float, extraction_rate: float, dt: float, steps: int) -> tuple[float, float]:
    stock = stock0
    cumulative_extraction = 0.0
    for _ in range(steps):
        extraction = min(stock, extraction_rate * dt)
        stock = max(0.0, stock - extraction)
        cumulative_extraction += extraction
    return stock, cumulative_extraction

def efficiency_adjusted_extraction(demand: float, efficiency_gain: float, rebound_factor: float) -> float:
    technical_reduction = demand * efficiency_gain
    rebound = technical_reduction * rebound_factor
    return max(0.0, demand - technical_reduction + rebound)

def build_parameter_records() -> list[ParameterRecord]:
    return [
        ParameterRecord("R0", 600.0, "stock units", "initial resource stock", "Stock definition and measurement boundary must be documented."),
        ParameterRecord("r", 0.18, "per year", "regeneration rate", "Regeneration may be seasonal, climate-dependent, or threshold-dependent."),
        ParameterRecord("K", 1000.0, "stock units", "carrying capacity", "Capacity can change with degradation, habitat, climate, or management."),
        ParameterRecord("H", 45.0, "stock units per year", "constant extraction or harvest", "Harvest should not be treated as controllable without governance assumptions."),
        ParameterRecord("A", 180.0, "stock units", "critical recovery threshold", "Threshold values require evidence and precaution."),
        ParameterRecord("loss_rate", 0.02, "per year", "additional degradation or leakage loss", "Hidden loss terms can make sustainability claims misleading."),
        ParameterRecord("efficiency_gain", 0.15, "fraction", "resource-use efficiency improvement", "Efficiency can create rebound if demand rises."),
    ]

def build_scenarios() -> list[ScenarioRecord]:
    dt = 0.1
    t = 80.0
    steps = int(t / dt)

    baseline_stock, baseline_extraction = simulate_resource(
        600.0,
        lambda stock: logistic_regeneration(stock, 0.18, 1000.0),
        35.0,
        dt,
        steps
    )

    high_harvest_stock, high_harvest_extraction = simulate_resource(
        600.0,
        lambda stock: logistic_regeneration(stock, 0.18, 1000.0),
        60.0,
        dt,
        steps
    )

    threshold_stock, threshold_extraction = simulate_resource(
        600.0,
        lambda stock: threshold_regeneration(stock, 0.18, 1000.0, 180.0),
        45.0,
        dt,
        steps
    )

    degraded_stock, degraded_extraction = simulate_resource(
        600.0,
        lambda stock: logistic_regeneration(stock, 0.18, 1000.0),
        45.0,
        dt,
        steps,
        loss_rate=0.02
    )

    nonrenewable_stock, nonrenewable_extraction = simulate_nonrenewable(
        600.0,
        30.0,
        dt,
        steps
    )

    adjusted_extraction = efficiency_adjusted_extraction(60.0, 0.15, 0.6)
    efficiency_stock, efficiency_extraction = simulate_resource(
        600.0,
        lambda stock: logistic_regeneration(stock, 0.18, 1000.0),
        adjusted_extraction,
        dt,
        steps
    )

    return [
        ScenarioRecord("renewable_precautionary_harvest", "renewable_logistic", t, baseline_stock, baseline_extraction, "harvest below idealized maximum yield allows persistence under baseline assumptions"),
        ScenarioRecord("renewable_high_harvest", "renewable_logistic", t, high_harvest_stock, high_harvest_extraction, "higher harvest pressure can push stock downward"),
        ScenarioRecord("threshold_recovery_risk", "threshold_regeneration", t, threshold_stock, threshold_extraction, "threshold-dependent recovery can slow or fail under depletion"),
        ScenarioRecord("degradation_loss_case", "renewable_with_loss", t, degraded_stock, degraded_extraction, "additional loss or degradation can undermine apparent sustainability"),
        ScenarioRecord("nonrenewable_drawdown", "nonrenewable", t, nonrenewable_stock, nonrenewable_extraction, "nonrenewable resource declines through extraction without regeneration"),
        ScenarioRecord("efficiency_with_rebound", "efficiency_rebound", t, efficiency_stock, efficiency_extraction, "efficiency gains are partly offset by rebound demand"),
    ]

def build_yield_records() -> list[YieldRecord]:
    msy = maximum_sustainable_yield(0.18, 1000.0)
    return [
        YieldRecord(
            "logistic_msy_baseline",
            0.18,
            1000.0,
            msy,
            0.7 * msy,
            "MSY is not a safe target under uncertainty by default; precautionary harvest is lower."
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
    yields = [asdict(record) for record in build_yield_records()]

    write_csv(output_dir/"tables"/"resource_parameter_records.csv", parameters)
    write_csv(output_dir/"tables"/"resource_scenario_records.csv", scenarios)
    write_csv(output_dir/"tables"/"resource_yield_records.csv", yields)

    audit = {
        "parameter_records": parameters,
        "scenario_records": scenarios,
        "yield_records": yields,
        "interpretation_warning": "Resource model outputs depend on stock definitions, regeneration assumptions, extraction records, thresholds, governance, uncertainty, and claim boundaries."
    }
    (output_dir/"json"/"resource_depletion_regeneration_audit.json").write_text(json.dumps(audit, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Resource Depletion and Regeneration Audit", "", "## Scenario Records"]
    for row in scenarios:
        report.append(f"- **{row['scenario_name']}** ({row['resource_type']}): final stock={row['final_stock']:.2f}, cumulative extraction={row['cumulative_extraction']:.2f}. {row['interpretation']}.")
    report += ["", "## Yield Records"]
    for row in yields:
        report.append(f"- **{row['record_name']}**: MSY={row['maximum_sustainable_yield']:.2f}, precautionary yield={row['precautionary_yield']:.2f}. {row['warning']}")
    report.append("")
    report.append("Resource model outputs depend on stock definitions, regeneration assumptions, extraction records, thresholds, governance, uncertainty, and claim boundaries.")
    (output_dir/"reports"/"resource_depletion_regeneration_audit.md").write_text("\n".join(report)+"\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Resource depletion and regeneration audit outputs generated.")

if __name__ == "__main__":
    main()
