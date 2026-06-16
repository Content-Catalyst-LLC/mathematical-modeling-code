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
    final_output: float
    final_capital: float
    interpretation: str

@dataclass(frozen=True)
class GrowthRecord:
    record_name: str
    initial_output: float
    growth_rate: float
    horizon: float
    final_output: float
    doubling_time: float
    warning: str

def exponential_output(y0: float, g: float, t: float) -> float:
    return y0 * math.exp(g * t)

def doubling_time(g: float) -> float:
    if g <= 0:
        return math.inf
    return math.log(2) / g

def logistic_output(y0: float, r: float, k: float, dt: float, steps: int) -> float:
    y = y0
    for _ in range(steps):
        y = max(0.0, y + r * y * (1 - y / k) * dt)
    return y

def simulate_capital(k0: float, y0: float, savings_rate: float, depreciation: float, productivity_growth: float, dt: float, steps: int) -> tuple[float, float]:
    capital = k0
    output = y0
    for _ in range(steps):
        investment = savings_rate * output
        capital = max(0.0, capital + (investment - depreciation * capital) * dt)
        output = output * math.exp(productivity_growth * dt) * (1 + 0.0005 * (capital - k0) * dt)
    return output, capital

def simulate_adjustment(x0: float, target: float, adjustment_speed: float, shock: float, shock_time: int, dt: float, steps: int) -> float:
    x = x0
    for step in range(steps):
        current_target = target + shock if step == shock_time else target
        x = x + adjustment_speed * (current_target - x) * dt
    return x

def cobb_douglas(a: float, k: float, l: float, alpha: float) -> float:
    return a * (k ** alpha) * (l ** (1 - alpha))

def growth_accounting(a_growth: float, k_growth: float, l_growth: float, alpha: float) -> float:
    return a_growth + alpha * k_growth + (1 - alpha) * l_growth

def build_parameter_records() -> list[ParameterRecord]:
    return [
        ParameterRecord("Y0", 100.0, "index", "initial output index", "Output measure and price basis must be documented."),
        ParameterRecord("g", 0.025, "per year", "baseline output growth rate", "Growth-rate assumptions compound strongly over time."),
        ParameterRecord("s", 0.22, "share of output", "investment or savings share", "Savings does not automatically become productive investment."),
        ParameterRecord("delta", 0.05, "per year", "depreciation rate", "Depreciation should include maintenance and obsolescence assumptions."),
        ParameterRecord("A_growth", 0.012, "per year", "productivity growth rate", "Productivity should not be used as an unexplained residual without interpretation."),
        ParameterRecord("lambda", 0.35, "per year", "adjustment speed", "Adjustment speed depends on institutions, frictions, contracts, and expectations."),
        ParameterRecord("capacity_limit", 240.0, "output index", "illustrative output constraint", "Constrained growth requires a defined mechanism and boundary."),
    ]

def build_scenarios() -> list[ScenarioRecord]:
    years = 40.0
    dt = 0.1
    steps = int(years / dt)
    exponential = exponential_output(100.0, 0.025, years)
    constrained = logistic_output(100.0, 0.06, 240.0, dt, steps)
    capital_output, capital_stock = simulate_capital(300.0, 100.0, 0.22, 0.05, 0.012, dt, steps)
    adjustment_output = simulate_adjustment(100.0, 160.0, 0.35, -30.0, 80, dt, steps)
    production_output = cobb_douglas(1.2, 450.0, 180.0, 0.35)
    return [
        ScenarioRecord("constant_growth_projection", "exponential_growth", years, exponential, 0.0, "constant proportional growth compounds over time"),
        ScenarioRecord("capacity_constrained_growth", "logistic_constraint", years, constrained, 0.0, "growth slows near a defined capacity or saturation limit"),
        ScenarioRecord("capital_accumulation_case", "capital_stock_flow", years, capital_output, capital_stock, "investment and depreciation shape long-run output capacity"),
        ScenarioRecord("adjustment_after_shock", "target_adjustment", years, adjustment_output, 0.0, "adjustment speed and shocks shape convergence dynamics"),
        ScenarioRecord("production_function_case", "cobb_douglas", years, production_output, 450.0, "production function output depends on productivity, capital, labor, and elasticity assumptions"),
    ]

def build_growth_records() -> list[GrowthRecord]:
    rows = []
    for g in [0.01, 0.025, 0.04]:
        rows.append(
            GrowthRecord(
                f"growth_rate_{g:.3f}",
                100.0,
                g,
                40.0,
                exponential_output(100.0, g, 40.0),
                doubling_time(g),
                "Growth-rate assumptions compound strongly over time."
            )
        )
    return rows

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
    growth_records = [asdict(record) for record in build_growth_records()]

    write_csv(output_dir/"tables"/"economic_parameter_records.csv", parameters)
    write_csv(output_dir/"tables"/"economic_scenario_records.csv", scenarios)
    write_csv(output_dir/"tables"/"economic_growth_records.csv", growth_records)

    audit = {
        "parameter_records": parameters,
        "scenario_records": scenarios,
        "growth_records": growth_records,
        "interpretation_warning": "Economic growth model outputs depend on output definitions, growth mechanisms, productivity assumptions, capital measurement, depreciation, constraints, shocks, distribution, uncertainty, and claim boundaries."
    }
    (output_dir/"json"/"economic_growth_adjustment_audit.json").write_text(json.dumps(audit, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Economic Growth and Adjustment Audit", "", "## Scenario Records"]
    for row in scenarios:
        report.append(f"- **{row['scenario_name']}** ({row['model_type']}): final output={row['final_output']:.2f}, final capital={row['final_capital']:.2f}. {row['interpretation']}.")
    report += ["", "## Growth Records"]
    for row in growth_records:
        report.append(f"- **{row['record_name']}**: final output={row['final_output']:.2f}; doubling time={row['doubling_time']:.2f}. {row['warning']}")
    report.append("")
    report.append("Economic growth model outputs depend on output definitions, growth mechanisms, productivity assumptions, capital measurement, depreciation, constraints, shocks, distribution, uncertainty, and claim boundaries.")
    (output_dir/"reports"/"economic_growth_adjustment_audit.md").write_text("\n".join(report)+"\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Economic growth and adjustment audit outputs generated.")

if __name__ == "__main__":
    main()
