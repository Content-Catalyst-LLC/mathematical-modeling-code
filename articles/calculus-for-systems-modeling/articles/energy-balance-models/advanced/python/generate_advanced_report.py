from pathlib import Path
import csv, json
ROOT = Path(__file__).resolve().parents[1]
out = ROOT / "outputs"
(out/"tables").mkdir(parents=True, exist_ok=True)
(out/"reports").mkdir(parents=True, exist_ok=True)
(out/"json").mkdir(parents=True, exist_ok=True)
rows = []
for feedback in [0.8, 1.0, 1.2, 1.5, 1.8]:
    forcing = 3.7
    heat_capacity = 10.0
    rows.append({
        "forcing": forcing,
        "feedback": feedback,
        "heat_capacity": heat_capacity,
        "equilibrium_temperature": forcing / feedback,
        "adjustment_time": heat_capacity / feedback,
        "governance_status": "review",
        "warning": "Feedback and heat-capacity sensitivity should be interpreted with boundary and reservoir assumptions."
    })
with (out/"tables"/"advanced_energy_balance_feedback_sweep.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)
audit = {
    "article": "Energy Balance Models",
    "advanced_standard": True,
    "features": ["one-layer energy balance", "two-layer heat uptake", "absorbed solar radiation", "surface energy partitioning", "equilibrium temperature", "adjustment time", "forcing and feedback sensitivity", "calculator layer", "Catalyst Canvas governance"],
    "warnings": ["Energy balance conclusions are not meaningful without a defined boundary.", "Equilibrium should not be confused with immediate response.", "Feedback terms can hide multiple physical processes.", "A model can fit temperature while misrepresenting mechanism."]
}
(out/"json"/"advanced_energy_balance_audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
(out/"reports"/"advanced_energy_balance_audit.md").write_text("# Advanced Energy Balance Model Audit\n\nIncludes one-layer and two-layer energy balance, absorbed solar radiation, surface energy partitioning, equilibrium response, adjustment time, sensitivity, calculators, and Canvas artifacts.\n", encoding="utf-8")
print("Advanced energy balance audit generated.")
