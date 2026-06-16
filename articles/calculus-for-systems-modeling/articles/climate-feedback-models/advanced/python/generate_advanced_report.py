from pathlib import Path
import csv, json, math

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / "outputs"
(out/"tables").mkdir(parents=True, exist_ok=True)
(out/"reports").mkdir(parents=True, exist_ok=True)
(out/"json").mkdir(parents=True, exist_ok=True)

forcing = 3.7
heat_capacity = 8.0
rows = []
for feedback in [0.9, 1.2, 1.6]:
    equilibrium = forcing / feedback
    response_80 = equilibrium * (1.0 - math.exp(-(feedback / heat_capacity) * 80.0))
    rows.append({
        "feedback": feedback,
        "equilibrium_temperature": equilibrium,
        "temperature_80yr": response_80,
        "sensitivity_to_lambda": -forcing / (feedback ** 2),
        "warning": "Feedback sign convention and uncertainty must be documented."
    })

with (out/"tables"/"advanced_climate_feedback_sweep.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

audit = {
    "article": "Case Study: Climate Feedback Models",
    "advanced_standard": True,
    "features": [
        "one-box energy balance",
        "two-box ocean uptake",
        "CO2 forcing",
        "feedback sensitivity",
        "carbon-cycle feedback",
        "threshold notes",
        "sign-convention governance",
        "calculator layer",
        "Catalyst Canvas governance"
    ],
    "warnings": [
        "Feedback signs must be stated before comparing parameters.",
        "Equilibrium response should not be confused with near-term forecast.",
        "Net feedback values can hide component uncertainty.",
        "Scenario assumptions should not be presented as predictions."
    ]
}

(out/"json"/"advanced_climate_feedback_audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
(out/"reports"/"advanced_climate_feedback_audit.md").write_text(
    "# Advanced Climate Feedback Models Audit\n\n"
    "Includes one-box energy balance, two-box ocean uptake, CO2 forcing, feedback sensitivity, carbon-cycle feedback, threshold notes, sign-convention governance, calculators, and Canvas artifacts.\n",
    encoding="utf-8"
)
print("Advanced climate feedback audit generated.")
