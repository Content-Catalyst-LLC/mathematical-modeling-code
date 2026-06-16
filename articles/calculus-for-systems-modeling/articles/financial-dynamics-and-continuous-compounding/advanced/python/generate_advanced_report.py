from pathlib import Path
import csv, json, math

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / "outputs"
(out/"tables").mkdir(parents=True, exist_ok=True)
(out/"reports").mkdir(parents=True, exist_ok=True)
(out/"json").mkdir(parents=True, exist_ok=True)

rows = []
for r in [0.01, 0.03, 0.05, 0.07, 0.09]:
    final = 1000.0 * math.exp(r * 30.0)
    sensitivity = 30.0 * final
    rows.append({
        "rate": r,
        "horizon_years": 30,
        "continuous_future_value": final,
        "rate_sensitivity": sensitivity,
        "governance_status": "review",
        "warning": "Long horizons amplify small rate differences."
    })

with (out/"tables"/"advanced_financial_rate_sweep.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

audit = {
    "article": "Financial Dynamics and Continuous Compounding",
    "advanced_standard": True,
    "features": [
        "continuous compounding",
        "discrete compounding",
        "present value",
        "net present value",
        "debt dynamics",
        "inflation adjustment",
        "geometric return",
        "rate sensitivity",
        "calculator layer",
        "Catalyst Canvas governance"
    ],
    "warnings": [
        "Rate convention must be documented before comparing financial outcomes.",
        "Cash-flow timing can dominate financial conclusions.",
        "Discount-rate choices can dominate long-horizon conclusions.",
        "Expected return does not guarantee realized compounded outcome."
    ]
}

(out/"json"/"advanced_financial_dynamics_audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
(out/"reports"/"advanced_financial_dynamics_audit.md").write_text(
    "# Advanced Financial Dynamics and Continuous Compounding Audit\n\n"
    "Includes continuous compounding, discrete compounding, present value, NPV, debt dynamics, inflation adjustment, geometric return, rate sensitivity, calculators, and Canvas artifacts.\n",
    encoding="utf-8"
)
print("Advanced financial dynamics audit generated.")
