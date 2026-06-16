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
    final_value: float
    present_value: float
    interpretation: str

@dataclass(frozen=True)
class RateRecord:
    record_name: str
    nominal_rate: float
    inflation_rate: float
    real_rate: float
    continuous_equivalent: float
    warning: str

def continuous_future_value(v0: float, r: float, t: float) -> float:
    return v0 * math.exp(r * t)

def continuous_present_value(fv: float, r: float, t: float) -> float:
    return fv * math.exp(-r * t)

def discrete_compound_value(v0: float, r: float, n: int, t: float) -> float:
    return v0 * (1 + r / n) ** (n * t)

def continuous_equivalent_rate(effective_rate: float) -> float:
    return math.log(1 + effective_rate)

def real_rate(nominal_rate: float, inflation_rate: float) -> float:
    return (1 + nominal_rate) / (1 + inflation_rate) - 1

def net_present_value(cash_flows: list[tuple[float, float]], discount_rate: float) -> float:
    return sum(amount * math.exp(-discount_rate * time) for time, amount in cash_flows)

def simulate_debt(balance0: float, rate: float, payment: float, dt: float, steps: int) -> float:
    balance = balance0
    for _ in range(steps):
        balance = max(0.0, balance + rate * balance * dt - payment * dt)
    return balance

def geometric_mean_return(returns: list[float]) -> float:
    product = 1.0
    for r in returns:
        product *= (1 + r)
    return product ** (1 / len(returns)) - 1

def leverage_ratio(assets: float, equity: float) -> float:
    return assets / equity if equity else math.inf

def rate_sensitivity(v0: float, r: float, t: float) -> float:
    return t * v0 * math.exp(r * t)

def build_parameter_records() -> list[ParameterRecord]:
    return [
        ParameterRecord("V0", 1000.0, "currency units", "initial value or principal", "Initial value must match the modeled account, asset, or debt balance."),
        ParameterRecord("r", 0.05, "per year", "interest, return, or discount rate", "Rate convention must be documented as nominal, real, effective, or continuous."),
        ParameterRecord("t", 30.0, "years", "time horizon", "Long horizons amplify small rate differences."),
        ParameterRecord("n", 12.0, "compounding periods per year", "discrete compounding frequency", "Compounding convention should match the contract or model purpose."),
        ParameterRecord("pi", 0.025, "per year", "inflation rate", "Cash flows and rates should use consistent real or nominal units."),
        ParameterRecord("sigma", 0.18, "annualized volatility", "volatility estimate", "Expected return does not guarantee realized compounded outcome."),
        ParameterRecord("payment", 80.0, "currency units per year", "debt repayment flow", "Debt may grow if payment does not exceed interest accumulation."),
    ]

def build_scenarios() -> list[ScenarioRecord]:
    continuous = continuous_future_value(1000.0, 0.05, 30.0)
    discrete = discrete_compound_value(1000.0, 0.05, 12, 30.0)
    discounted = continuous_present_value(5000.0, 0.05, 30.0)
    npv = net_present_value([(0, -1000), (5, 300), (10, 500), (15, 900), (20, 1200)], 0.045)
    debt = simulate_debt(2000.0, 0.07, 120.0, 0.1, 300)
    rr = real_rate(0.06, 0.025)
    real_growth = continuous_future_value(1000.0, rr, 30.0)
    geometric = geometric_mean_return([0.08, -0.12, 0.15, 0.04, -0.05, 0.11])
    levered = leverage_ratio(5000.0, 1000.0)
    sensitivity = rate_sensitivity(1000.0, 0.05, 30.0)

    return [
        ScenarioRecord("continuous_compounding_case", "future_value", 30.0, continuous, 1000.0, "continuous compounding accumulates value exponentially"),
        ScenarioRecord("monthly_compounding_case", "discrete_compounding", 30.0, discrete, 1000.0, "discrete compounding depends on compounding frequency"),
        ScenarioRecord("discounted_future_value", "present_value", 30.0, 5000.0, discounted, "discounting translates future value into present value"),
        ScenarioRecord("cash_flow_npv", "net_present_value", 20.0, npv, npv, "cash-flow timing and discount rate determine net present value"),
        ScenarioRecord("debt_dynamics_case", "debt_balance", 30.0, debt, 0.0, "debt balance depends on interest, payments, and time"),
        ScenarioRecord("real_return_case", "inflation_adjusted_growth", 30.0, real_growth, 1000.0, "real growth adjusts nominal return for inflation"),
        ScenarioRecord("geometric_return_case", "portfolio_compounding", 6.0, geometric, 0.0, "geometric return reflects compounded path behavior"),
        ScenarioRecord("leverage_case", "leverage_ratio", 0.0, levered, 0.0, "leverage magnifies sensitivity to asset value changes"),
        ScenarioRecord("rate_sensitivity_case", "sensitivity", 30.0, sensitivity, 0.0, "value sensitivity to rate grows with time and accumulated value"),
    ]

def build_rate_records() -> list[RateRecord]:
    return [
        RateRecord(
            "nominal_to_real_rate_case",
            0.06,
            0.025,
            real_rate(0.06, 0.025),
            continuous_equivalent_rate(0.06),
            "Cash flows and rates should use consistent real or nominal units."
        ),
        RateRecord(
            "effective_to_continuous_case",
            0.05,
            0.0,
            0.05,
            continuous_equivalent_rate(0.05),
            "Continuous equivalent rate is a convention conversion, not a risk adjustment."
        ),
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
    rate_records = [asdict(record) for record in build_rate_records()]

    write_csv(output_dir/"tables"/"financial_parameter_records.csv", parameters)
    write_csv(output_dir/"tables"/"financial_scenario_records.csv", scenarios)
    write_csv(output_dir/"tables"/"financial_rate_records.csv", rate_records)

    audit = {
        "parameter_records": parameters,
        "scenario_records": scenarios,
        "rate_records": rate_records,
        "interpretation_warning": "Financial model outputs depend on rate convention, time horizon, cash-flow timing, compounding rule, inflation basis, risk, liquidity, fees, taxes, uncertainty, and claim boundaries."
    }
    (output_dir/"json"/"financial_dynamics_compounding_audit.json").write_text(json.dumps(audit, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Financial Dynamics and Continuous Compounding Audit", "", "## Scenario Records"]
    for row in scenarios:
        report.append(f"- **{row['scenario_name']}** ({row['model_type']}): final value={row['final_value']:.4f}, present value={row['present_value']:.4f}. {row['interpretation']}.")
    report += ["", "## Rate Records"]
    for row in rate_records:
        report.append(f"- **{row['record_name']}**: real rate={row['real_rate']:.6f}; continuous equivalent={row['continuous_equivalent']:.6f}. {row['warning']}")
    report.append("")
    report.append("Financial model outputs depend on rate convention, time horizon, cash-flow timing, compounding rule, inflation basis, risk, liquidity, fees, taxes, uncertainty, and claim boundaries.")
    (output_dir/"reports"/"financial_dynamics_compounding_audit.md").write_text("\n".join(report)+"\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Financial dynamics and continuous compounding audit outputs generated.")

if __name__ == "__main__":
    main()
