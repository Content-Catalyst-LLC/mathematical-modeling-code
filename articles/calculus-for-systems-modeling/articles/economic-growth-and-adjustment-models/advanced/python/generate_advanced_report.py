from pathlib import Path
import csv, json, math

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / "outputs"
(out/"tables").mkdir(parents=True, exist_ok=True)
(out/"reports").mkdir(parents=True, exist_ok=True)
(out/"json").mkdir(parents=True, exist_ok=True)

rows = []
for g in [0.01, 0.02, 0.025, 0.03, 0.04]:
    rows.append({
        "growth_rate": g,
        "horizon_years": 40,
        "final_output_index": 100.0 * math.exp(g * 40),
        "doubling_time": math.log(2) / g,
        "governance_status": "review",
        "warning": "Growth-rate assumptions compound strongly over time."
    })

with (out/"tables"/"advanced_growth_rate_sweep.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

audit = {
    "article": "Economic Growth and Adjustment Models",
    "advanced_standard": True,
    "features": [
        "exponential growth",
        "doubling time",
        "logistic constrained growth",
        "capital accumulation",
        "depreciation and investment",
        "production functions",
        "adjustment dynamics",
        "shock response",
        "calculator layer",
        "Catalyst Canvas governance"
    ],
    "warnings": [
        "Output growth should not be treated as complete social progress.",
        "Growth-rate assumptions compound strongly over time.",
        "Productivity should not be used as a residual without interpretation.",
        "Unconstrained growth assumptions should be compared with constrained scenarios."
    ]
}

(out/"json"/"advanced_economic_growth_audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
(out/"reports"/"advanced_economic_growth_audit.md").write_text(
    "# Advanced Economic Growth and Adjustment Audit\n\n"
    "Includes exponential growth, doubling time, constrained growth, capital accumulation, productivity assumptions, adjustment dynamics, shocks, calculators, and Canvas artifacts.\n",
    encoding="utf-8"
)
print("Advanced economic growth audit generated.")
