from pathlib import Path
import csv, json, math
ROOT = Path(__file__).resolve().parents[1]
out = ROOT / "outputs"
(out/"tables").mkdir(parents=True, exist_ok=True)
(out/"reports").mkdir(parents=True, exist_ok=True)
(out/"json").mkdir(parents=True, exist_ok=True)
rows = []
n0, r, k = 100.0, 0.08, 1000.0
for t in range(0, 41, 5):
    expn = n0 * math.exp(r*t)
    logn = k / (1 + ((k-n0)/n0)*math.exp(-r*t))
    rows.append({"time": t, "exponential": expn, "logistic": logn, "gap": expn-logn})
with (out/"tables"/"advanced_population_growth_comparison.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader(); writer.writerows(rows)
audit = {
    "article": "Case Study: Modeling Population Dynamics",
    "advanced_standard": True,
    "features": ["Allee effect", "harvesting", "stochastic paths", "Leslie projection", "two-patch migration", "diffusion step", "calibration grid", "identifiability diagnostics"],
    "warnings": ["A growth law is an assumption, not a universal description.", "Carrying capacity is assumption-bearing and may change over time.", "Threshold parameters can be difficult to identify from limited data.", "A fitted curve does not automatically prove the model mechanism.", "A single stochastic path is not a distribution."]
}
(out/"json"/"advanced_population_dynamics_audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
(out/"reports"/"advanced_population_dynamics_audit.md").write_text("# Advanced Population Dynamics Audit\n\nIncludes Allee effects, harvesting, stochastic paths, structured populations, spatial migration, calibration, identifiability diagnostics, calculators, and Canvas governance.\n", encoding="utf-8")
print("Advanced population dynamics audit generated.")
